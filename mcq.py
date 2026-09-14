import re
from pathlib import Path
from tex2moodle import tex2moodle

def mcq2moodle(myLaTeXfile: Path) -> None:
	"""Convert supported LaTeX multiple-choice question file to Moodle-compatible XML format."""
	myLaTeXtext = myLaTeXfile.read_text(encoding="utf-8")

	# Prepare question
	## Extract the question text: everything between \question and \begin{mychoices}
	myMatch = re.search(
		r"\\question\b\s*(?:\[[^\]]*\])?\s*(.*?)\\begin\{mychoices\}",
		myLaTeXtext,
		re.DOTALL
	)

	if myMatch is None:
		raise ValueError("Question not found.")

	myLaTeXquestion = myMatch.group(1).strip()

	## Convert the question text for Moodle
	myXMLquestion = tex2moodle(myLaTeXquestion)

	# Prepare choices
	## Extract everything inside the mychoices environment
	myMatch = re.search(
		r"\\begin\{mychoices\}(.*?)\\end\{mychoices\}",
		myLaTeXtext,
		re.DOTALL
	)

	if myMatch is None:
		raise ValueError("Choices not found.")

	myLaTeXchoices = myMatch.group(1).strip()

	## Separate individual choices
	myChoices = re.findall(
		r"\\(CorrectChoice|choice)\b\s*(.*?)(?=\\(?:CorrectChoice|choice)\b|\Z)",
		myLaTeXchoices,
		re.DOTALL
	)

	## Convert each choice for Moodle
	myXMLchoices = []

	for myType, myText in myChoices:
		myXMLtext = tex2moodle(myText.strip())
		myXMLchoices.append((myType, myXMLtext))

	# Write the XML file
	## Start the XML document with the question
	myXML = f"""<?xml version="1.0" encoding="UTF-8"?>
  <quiz>
    <question type="multichoice">
      <name>
        <text>
          {myLaTeXfile.stem}
        </text>
      </name>
      <questiontext format="html">
        <text>
          <![CDATA[
            {myXMLquestion}
          ]]>
        </text>
      </questiontext>
      <single>true</single>
      <shuffleanswers>1</shuffleanswers>
  """

	## Add the choices
	myWrongFraction = -100 / len(myXMLchoices)

	for myType, myText in myXMLchoices:
		if myType == "CorrectChoice":
			myFraction = 100
		else:
			myFraction = myWrongFraction

		myXML += f"""    <answer fraction="{myFraction}">
        <text>
          <![CDATA[
            {myText}
          ]]>
        </text>
      </answer>
  """

	## Close the question and the XML document
	myXML += """  </question>
  </quiz>
  """

	# Save the XML beside the original LaTeX file
	myXMLfile = myLaTeXfile.with_suffix(".xml")
	myXMLfile.write_text(myXML, encoding="utf-8")
