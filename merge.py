from pathlib import Path
from typing import List


def merge2moodle(myFolder: Path, myPrefix: str) -> List[Path]:
	"""Merge matching Moodle XML files and return the source XML paths."""

	# Define the merged output filename.
	myXMLfile = myFolder / f"{myPrefix}2moodle.xml"

	# Select matching XML files in filename order, excluding the output.
	myXMLfiles = sorted(
		myFile
		for myFile in myFolder.iterdir()
		if myFile.name.startswith(myPrefix)
		and myFile.suffix == ".xml"
		and myFile.is_file()
		and myFile != myXMLfile
	)

	# Start the combined XML document.
	myXML = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n'

	# Append the contents inside each source file's quiz element.
	for myFile in myXMLfiles:
		try:
			myXMLtext = myFile.read_text(encoding="utf-8")
		except (OSError, UnicodeError) as myError:
			raise RuntimeError(
				f"Could not read the XML file as UTF-8:\n"
				f"{myFile.resolve()}"
			) from myError

		# Check the expected delimiters before extracting the contents.
		myQuizStart = myXMLtext.find("<quiz>")
		myQuizEnd = myXMLtext.rfind("</quiz>")

		if myQuizStart == -1 or myQuizEnd < myQuizStart + len("<quiz>"):
			raise ValueError(
				f"Cannot merge XML file: {myFile.resolve()}\n"
				"Expected <quiz> followed by </quiz>.\n\n"
				f"XML content:\n{myXMLtext}"
			)

		myXMLtext = myXMLtext.split("<quiz>", 1)[1].rsplit("</quiz>", 1)[0]
		myXML += myXMLtext.strip() + "\n"

	# Close and save the combined XML document.
	myXML += "</quiz>\n"
	try:
		myXMLfile.write_text(myXML, encoding="utf-8")
	except (OSError, UnicodeError) as myError:
		raise RuntimeError(
			f"Could not write the merged XML file:\n"
			f"{myXMLfile.resolve()}\n"
			"Individual XML files have not been deleted."
		) from myError

	# Return the source paths so main.py can delete them after merging.
	return myXMLfiles