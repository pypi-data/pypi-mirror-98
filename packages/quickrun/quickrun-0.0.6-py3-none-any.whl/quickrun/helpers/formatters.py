"""
Collection of output formatters
Each function takes the Base.state and will format and display the state
"""


from rich.console import Console as RichConsole
from rich.table import Table as RichTable


def default(state):
	for result in state.get("output", []):
		print(result)


def none(_):
	pass


def fake_shell(state):
	console = RichConsole()
	for result in state.get("output", []):
		server, host, command, output = (
			result["server"],
			result["host"],
			result["command"],
			result["output"],
		)
		console.print(f"ubuntu@{host}|{server} $ {command}")
		console.print(output)
		console.print()


def table(state):
	table = RichTable(title="Results")

	data = state.get("output", [])
	if len(data) > 0:
		for column in data[0].keys():
			table.add_column(column)

	for item in data:
		table.add_row(*item.values())

	RichConsole().print(table)
