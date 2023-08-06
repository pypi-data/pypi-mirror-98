"""
Basic wrapper around pexpect.pxssh
"""

from pexpect import pxssh


class ssh:
	def __init__(self, server, user, pw=None, login_timeout=5):
		self.ssh = pxssh.pxssh()
		self.server = server
		self.user = user

		try:
			self.ssh.login(server, user, pw, login_timeout=login_timeout)
		except pxssh.ExceptionPxssh:
			raise Exception(f"SSH to {server} failed, bad credentials or ip type?")

	def run(self, cmd, strip_cmd=False, with_exit=False):
		self.ssh.sendline(cmd)
		self.ssh.prompt()
		out = self.ssh.before.decode("utf-8")

		# `out` also contains the command we ran
		# so count newlines in cmd and ignore that many lines
		if strip_cmd:
			cmd_index = cmd.count("\n") or 1
			out = "\n".join(out.split("\n")[cmd_index:])

		if with_exit:
			return out, self.get_exit_code()

		return out

	def test(self, cmd):
		# Ignore all output
		cmd += " >/dev/null 2>&1"
		self.run(cmd)
		return self.get_exit_code()

	def get_exit_code(self):
		code = self.run("echo $?", strip_cmd=True).rstrip()
		return int(code)

	def end(self):
		self.ssh.logout()
