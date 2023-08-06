"""
A collection of CLI helper methods
"""

import typing
from typing import Optional

def challenge(expect: str, msg: Optional[str]=None) -> bool:
	"""
	Prompt user to enter an expected value as confirmation
	"""
	if msg:
		print(msg)

	challenge = input(f"Enter '{expect}' to continue: ")
	try:
		if challenge != str(expect):
			return False
	except ValueError:
		return False

	return True

