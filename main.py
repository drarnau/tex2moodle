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
			myParser.error(f"File not found: {myLaTeXfile}")

		myLaTeXfiles = [myLaTeXfile]

	else:
		# Select .tex files beginning with the prefix, in filename order.
		# Search only the folder where the command was run.
		myLaTeXfiles = sorted(
			myFile
			for myFile in myFolder.iterdir()
			if myFile.name.startswith(myInput)
			and myFile.suffix == ".tex"
			and myFile.is_file()
		)

		# Stop if no LaTeX files match the prefix.
		if not myLaTeXfiles:
			myParser.error(
				f"No .tex files starting with '{myInput}' in the current folder."
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
			myXMLfile.unlink()

# Run the program when this file is executed directly.
if __name__ == "__main__":
	main()