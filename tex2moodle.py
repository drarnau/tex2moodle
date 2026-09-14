import re

def inlinemath2moodle(match):
	r"""Prepare inline maths for Moodle-compatible XML text:
	(1) Add spaces around literal <, >, and & (in case there are not).
	(2) Substitute $...$ with \(...\).
	"""
	# Use text within $...$ (exlude $ signs)
	mymathtex = match.group(1)

	# Add spaces around literal <, >, and & (in case there are not)
	## Add a missing space before
	mymathtex = re.sub(
		r"(?<![\\ ])([<>&])",
		r" \1",
		mymathtex,
	)

	## Add a missing space after the character
	mymathtex = re.sub(
		r"(?<!\\)([<>&])(?! )",
		r"\1 ",
		mymathtex,
	)

	# Substiute $...$ with \(...\)
	return rf"\({mymathtex}\)"

def tex2moodle(mytex: str) -> str:
	"""Convert supported LaTeX text to Moodle-compatible XML text."""

	# Convert simple subsection headings (\subsection*{})
	mytex = re.sub(
		r"\\subsection\*\{([^{}]*)\}",
		r"<h3>\1</h3>",
		mytex,
	)

	## Convert inline math (cath everything between $...$)
	mytex = re.sub(
		r"\$([^$]*)\$",
		inlinemath2moodle,
		mytex,
	)

	return mytex