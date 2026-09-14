# Import argument handling, file paths and the conversion functions.
import argparse
from pathlib import Path
from desc import desc2moodle
from mcq import mcq2moodle
from merge import merge2moodle

def main():
	# Define the command and its required argument.
	myParser = argparse.ArgumentParser(
		prog="tex2moodle",
		description="Convert supported LaTeX files to Moodle XML.",
	)
	myParser.add_argument(
		"input",
		help="A supported LaTeX file or a filename prefix in the current folder.",
	)

	# Read the argument and identify the folder where the command was run.
	myArgs = myParser.parse_args()
	myInput = myArgs.input
	myFolder = Path.cwd()

	# If the argument ends in .tex, select that single file.
	if myInput.endswith(".tex"):
		myLaTeXfile = Path(myInput)

		# Stop if the supplied file does not exist.
		if not myLaTeXfile.is_file():
			myParser.error(
				f"Input is not an existing file: {myLaTeXfile.resolve()}"
			)

		myLaTeXfiles = [myLaTeXfile]

	else:
		# Select matching .tex files, excluding names ending in _ChatGPT.
		myLaTeXfiles = sorted(
			myFile
			for myFile in myFolder.iterdir()
			if myFile.name.startswith(myInput)
			and myFile.suffix == ".tex"
			and not myFile.stem.lower().endswith("_chatgpt")
			and myFile.is_file()
		)

		# Stop if no LaTeX files match the prefix.
		if not myLaTeXfiles:
			myParser.error(
				f"No .tex files starting with '{myInput}' in:\n"
				f"{myFolder}\n"
				"Files ending in _chatgpt before .tex are excluded "
				"(ignoring case)."
			)

	# Convert each selected supported LaTeX file into an individual XML file.
	for myLaTeXfile in myLaTeXfiles:
		# Filenames containing "description" are converted as descriptions.
		if "description" in myLaTeXfile.name:
			desc2moodle(myLaTeXfile)

		# Other filenames are converted as multiple-choice questions.
		else:
			mcq2moodle(myLaTeXfile)

	# For a prefix, merge the matching XML files into <prefix>2moodle.xml.
	# For a single .tex argument, keep its individual XML file.
	if not myInput.endswith(".tex"):
		myXMLfiles = merge2moodle(myFolder, myInput)

		# Delete only the source XML files returned by the successful merge.
		# The merged output is excluded from this list by merge2moodle().
		for myXMLfile in myXMLfiles:
			try:
				myXMLfile.unlink()
			except OSError as myError:
				myMergedXMLfile = myFolder / f"{myInput}2moodle.xml"
				raise RuntimeError(
					f"Merged XML saved to: {myMergedXMLfile}\n"
					f"Could not delete individual XML file: "
					f"{myXMLfile.resolve()}"
				) from myError

# Run the program when this file is executed directly.
if __name__ == "__main__":
	main()