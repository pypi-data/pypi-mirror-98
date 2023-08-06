"""
Helpers for finding servers using the AWS CLI
NOTE: Just calls the aws cli directly
"""

import os, sys, json, typing, subprocess, jq

def _build_filter(search: dict, contains=False):
	"""
	Take a dict of aws cli filters and return as list in correct format
	"""
	filters = []
	for name, value in search.items():
		if contains:
			value = f'*{value}*'
		filters.append(f'"Name={name},Values={value}"')
	
	return filters


def _find_tag(tags: dict, key: str):
	"""
	Get the value of a tag from the tags array
	"""
	return next(filter(lambda x: x["Key"] == key, tags))["Value"]


def find_instances(search: dict={}, contains: bool=False, running_only: bool=True, region: str="eu-west-2", raw: bool=False):
	"""
	Takes an instance name and optional region and returns the instanceId, PublicIp, PrivateIp and Tags

	search:       a dictionary of filters to pass to aws cli
	contains:     helper to automatically wrap filter value in asterisks
	running_only: filters out non running instances
	region:       the aws region
	raw:          returns raw output from aws cli
	"""

	filters = _build_filter(search, contains)

	# Ignore non running instances
	if running_only:
		filters.append('"Name=instance-state-name,Values=running"')

	filters = ' '.join(filters)
	command = f'aws ec2 describe-instances --output json --filters {filters} --region {region}'

	proc = subprocess.Popen(
		command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
	)

	out, err = proc.communicate()

	if out.decode("utf-8").rstrip() == "null":
		raise Exception(f"Failed to get results from aws cli\n\n{command}")

	if err:
		raise Exception(err)

	if raw:
		return json.loads(out)

	results = jq\
		.compile('[.Reservations[].Instances[]] | map({ InstanceId, PublicIp: .PublicIpAddress, PrivateIp: .PrivateIpAddress, Tags })')\
		.input(text=out.decode("utf-8"))\
		.first()

	# Pull the name out of the tag and put it at the top level
	for result in results:
		result["Name"] = _find_tag(result["Tags"], "Name")

	return results
