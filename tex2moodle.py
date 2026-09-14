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

def list2moodle(match):
	"""Convert a simple LaTeX list to Moodle-compatible XML text."""
	myEnvironment = match.group(1)
	myContent = match.group(2)

	if myEnvironment == "itemize":
		myTag = "ul"
	else:
		myTag = "ol"

	myItems = re.split(r"\\item\b\s*", myContent)[1:]

	myXMLitems = "\n".join(
		f"<li>{myItem.strip()}</li>"
		for myItem in myItems
	)

	return f"<{myTag}>\n{myXMLitems}\n</{myTag}>"

def tex2moodle(mytex: str) -> str:
	"""Convert supported LaTeX text to Moodle-compatible XML text."""

	# Convert simple subsection headings (\subsection*{})
	mytex = re.sub(
		r"\\subsection\*\{([^{}]*)\}",
		r"<h3>\1</h3>",
		mytex,
	)

	# Convert simple numbered and unnumbered lists
	mytex = re.sub(
		r"\\begin\{(itemize|enumerate)\}(.*?)\\end\{\1\}",
		list2moodle,
		mytex,
		flags=re.DOTALL,
	)

	## Convert inline math (cath everything between $...$)
	mytex = re.sub(
		r"\$([^$]*)\$",
		inlinemath2moodle,
		mytex,
	)

	return mytex