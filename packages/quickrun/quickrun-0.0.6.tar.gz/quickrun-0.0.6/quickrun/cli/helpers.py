"""
A collection of CLI helper methods
"""

def challenge(msg, expect):
	"""
	Prompt user to verify the run will do what they expect
	"""
	print(msg)

	challenge = input(f"Enter '{expect}' to continue: ")
	try:
		if challenge != str(expect):
			return False
	except ValueError:
		return False

	return True

