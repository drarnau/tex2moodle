import argparse
from pathlib import Path
from desc import desc2moodle
from mcq import mcq2moodle


def main():
	myParser = argparse.ArgumentParser(
		prog="tex2moodle",
		description="Convert supported LaTeX files to Moodle XML.",
	)
	myParser.add_argument("file", type=Path)
	myArgs = myParser.parse_args()

	myLaTeXfile = myArgs.file

	if not myLaTeXfile.is_file():
		myParser.error(f"File not found: {myLaTeXfile}")

	if "description" in myLaTeXfile.name:
		desc2moodle(myLaTeXfile)
	else:
		mcq2moodle(myLaTeXfile)

if __name__ == "__main__":
	main()