from tex2moodle import tex2moodle
from pathlib import Path

def desc2moodle(myLaTeXfile: Path) -> None:
	"""Convert supported LaTeX exercise description file to Moodle XML format."""
	myLaTeXdesc = myLaTeXfile.read_text(encoding="utf-8")

	# Convert LaTeX to Moodle-compatible XML
	myXMLdesc = tex2moodle(myLaTeXdesc)

	# Wrap the converted content in Moodle XML
	myXML = f"""<?xml version="1.0" encoding="UTF-8"?>
    <quiz>
      <question type="description">
        <name>
          <text>{myLaTeXfile.stem}</text>
        </name>
      <questiontext format="html">
        <text>
          <![CDATA[
            {myXMLdesc}
          ]]>
        </text>
      </questiontext>
      </question>
    </quiz>
  """

	# Save the XML beside the original LaTeX file
	myXMLfile = myLaTeXfile.with_suffix(".xml")
	myXMLfile.write_text(myXML, encoding="utf-8")