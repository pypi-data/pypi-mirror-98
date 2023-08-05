"""
Wrapper around termcolor
"""

from rich.console import Console
from rich.table import Table


class Out:
	console = Console()

	@staticmethod
	def output(msg, *style, **kwargs):
		style = " ".join(style)
		Out.console.print(msg, style=style, **kwargs)

	@staticmethod
	def plain(msg, *style, **kwargs):
		Out.output(msg, *style)

	@staticmethod
	def info(msg, *style, **kwargs):
		Out.output(msg, "blue", *style)

	@staticmethod
	def success(msg, *style, **kwargs):
		Out.output(msg, "green", *style)

	@staticmethod
	def warning(msg, *style, **kwargs):
		Out.output(msg, "yellow", *style)

	@staticmethod
	def error(msg, *style, **kwargs):
		Out.output(msg, "red", *style)
