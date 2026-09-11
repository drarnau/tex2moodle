import sys
import re
from pathlib import Path

# Read the LaTeX file specified as a command-line argument
myLaTeXfile = Path(sys.argv[1]) 
myLaTeXtext = myLaTeXfile.read_text(encoding="utf-8")

# Convert LaTeX \subsection*{} to HTML <h3></h3>
myXMLtext = re.sub(
  r"\\subsection\*\{([^{}]*)\}",
  r"<h3>\1</h3>",
  myLaTeXtext
)

# Convert $...$ to \(...\)
myXMLtext = re.sub(
  r"\$([^$]*)\$",
  r"\\(\1\\)",
  myXMLtext
)

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
        {myXMLtext}
      ]]>
      </text>
    </questiontext>
  </question>
</quiz>
"""

# Save the XML beside the original LaTeX file
myXMLfile = myLaTeXfile.with_suffix(".xml")
myXMLfile.write_text(myXML, encoding="utf-8")