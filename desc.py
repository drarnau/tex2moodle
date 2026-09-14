from tex2moodle import tex2moodle
from pathlib import Path

def desc2moodle(myLaTeXfile: Path) -> None:
	"""Convert supported LaTeX exercise description file to Moodle XML format."""
	try:
		myLaTeXdesc = myLaTeXfile.read_text(encoding="utf-8")
	except (OSError, UnicodeError) as myError:
		raise RuntimeError(
			f"Could not read the LaTeX file as UTF-8:\n"
			f"{myLaTeXfile.resolve()}"
		) from myError

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
	try:
		myXMLfile.write_text(myXML, encoding="utf-8")
	except (OSError, UnicodeError) as myError:
		raise RuntimeError(
			f"Could not write the XML file:\n"
			f"{myXMLfile.resolve()}"
		) from myError