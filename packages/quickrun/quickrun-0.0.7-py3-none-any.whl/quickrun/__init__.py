#!/usr/bin/env python3

"""
This is the base module all other modules inherit from
It defines the basic outline runners should have and validates they are set correctly
"""

import sys
from typing import List, Dict, Optional
from dataclasses import dataclass

# Export our lib to callers
import quickrun.helpers.formatters as formatters
from quickrun.cli.ssh import ssh


__version__ = "0.0.7"


@dataclass
class Server:
	name: str  # A friendly name for this server
	host: str  # The IP or hostname to connect to
	user: str  # The user to connect as
	pw: Optional[str] = None  # Optional password - ssh keys are preferred

	@classmethod
	def from_list(cls, server_list, ip_type="PrivateIp", default_user="ubuntu"):
		"""
		Takes a list of server dicts and returns a List[Server]
		"""
		return list(map(lambda x: Server(
			name=x["Name"],
			host=x[ip_type],
			user=x.get("user", default_user)
		), server_list))


# A command object
@dataclass
class Command:
	name: str  # The name of the command
	cmd: str  # The command itself
	test: bool = False  # Whether this is a test
	expect_fail: bool = False  # Whether to treat non zero exit status as success


class QuickRun:
	def __init__(self):
		self.ok = True
		self.servers: List[Server] = []
		self.commands: List[Command] = []
		self.state: Dict[str, any] = {}
		self.formatter = formatters.default

		# Config
		self.store_state: bool = False

	# Run the commands
	def main(self):
		"""
		Main execution function
		"""
		# Ensure we have arrays
		self.servers = arr(self.servers)
		self.commands = arr(self.commands)

		# Check we actually have stuff to do
		if len(self.servers) == 0 or len(self.commands) == 0:
			print("Nothing to do")

		# Call our before_all hook
		self.before_all()

		# Go through all servers and commands and run them
		for server in self.servers:
			conn = self.connect(server)
			if not conn:
				continue

			for command in self.commands:
				self.run(conn, command, server)

		# Call our after_all hook
		return self.after_all()

	def connect(self, server: Server):
		"""
		Run prehook, Connect to server, run post hook
		Return ssh instance
		"""
		self.before_connection(server)

		try:
			conn = ssh(server.host, server.user)
		except Exception as e:
			print(
				f"Following error was raised during ssh to {server}: {e}",
				file=sys.stderr,
			)
			self.on_error(e, server=server, action="Connect")
			return

		self.after_connection(server)
		return conn

	def run(self, conn, command: Command, server: Server):
		"""
		Call pre hook, run command, call post hook
		"""
		self.before_command(server, command)

		try:
			output = conn.run(command.cmd, strip_cmd=True)
		except Exception as e:
			print(
				f"Following error was raised while running {command} on {server}: {e}",
				file=sys.stderr,
			)
			return self.on_error(e, server=server, command=command, action="Command")

		if "output" not in self.state:
			self.state["output"] = []

		self.state["output"].append(
			{
				"server": server.name,
				"host": server.host,
				"command": command.cmd.strip(),
				"output": output.strip(),
			}
		)

		self.after_command(server, command, output)

	def display(self):
		"""
		Display: Call out to the define formatter for displaying
		"""
		self.formatter(self.state)

	# == HOOKS ==#
	"""
	There are currently 7 types of hooks, and they
	run in the order that that they are defined below
	By default they all do nothing
	You are expected to override them in your run module
	eg. `self.hooks.before_all = lambda x: print("Starting...")`
	"""

	# before_all: Runs before anything is done
	def before_all(self):
		pass

	# before_connection: Runs before connecting to each server
	def before_connection(self, server):
		pass

	# after_connection: Runs after connecting to each server
	def after_connection(self, server):
		pass

	# before_command: Runs before each command is ran
	def before_command(self, server, command):
		pass

	# after_command: Runs after each command is ran
	def after_command(self, server, command, output):
		pass

	# after_all: Runs after everything is done
	def after_all(self):
		pass

	# on_error: Called when an error occurs
	def on_error(self, exception, **info):
		pass


# == HELPERS ==#
def arr(item):
	"""
	Ensure $item is a list
	"""
	if isinstance(item, list):
		return item
	return [item]
