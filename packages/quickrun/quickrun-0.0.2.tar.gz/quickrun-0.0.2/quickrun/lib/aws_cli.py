"""
Helpers for finding servers using the AWS CLI
NOTE: Just calls the aws cli directly
"""

import os, json, subprocess


def find_tag(tags, key):
	"""
	Get the value of a tag from the tags array
	"""
	return next(filter(lambda x: x["Key"] == key, tags))["Value"]


def find_instances(name, region="eu-west-2", exact=False):
	"""
	Takes an instance name and optional region and returns the instanceId, PublicIp, PrivateIp and Tags
	"""
	if not exact:
		name = f"*{name}*"

	aws = f'aws ec2 describe-instances --output json --filters "Name=tag:Name,Values={name}" "Name=instance-state-name,Values=running" --region {region}'
	jq = "jq '[.Reservations[].Instances[]] | map({ InstanceId, PublicIp: .PublicIpAddress, PrivateIp: .PrivateIpAddress, Tags })'"
	command = f"{aws} | {jq}"

	proc = subprocess.Popen(
		command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
	)

	out, err = proc.communicate()

	if out.decode("utf-8").rstrip() == "null":
		raise Exception(f"Failed to get results from aws cli\n\n{command}")

	if err:
		raise Exception(err)

	results = json.loads(out)

	# Pull the name out of the tag and put it at the top level
	for result in results:
		result["Name"] = find_tag(result["Tags"], "Name")

	return results
