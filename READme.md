# tex2moodle

Small Python scripts that convert individual LaTeX snippets into Moodle XML.

Requires Python 3. No additional Python packages are needed.

## Usage

Run the appropriate script with the path to a LaTeX file:

```bash
python3 /path/to/tex2moodle/tex2moodle_desc.py description.tex
python3 /path/to/tex2moodle/tex2moodle_mcq.py question.tex
```

Replace `/path/to/tex2moodle` with the location of this project. Input files can live anywhere.

Each script saves an XML file beside the input file, using the same filename with an `.xml` extension. An existing output file is overwritten.

## Supported input

- `tex2moodle_desc.py`: creates a Moodle description and converts `\subsection*{...}` into an HTML heading.
- `tex2moodle_mcq.py`: creates a single-answer multiple-choice question from `\question` followed by a `mychoices` environment. Use one `\CorrectChoice` and mark the remaining answers with `\choice`.

Both scripts convert inline mathematics from `$...$` to `\(...\)`. They support specific LaTeX patterns rather than general LaTeX documents. See `tests/` for examples.

## Manual tests

From the project directory, run:

```bash
python3 tex2moodle_desc.py tests/description.tex
python3 tex2moodle_mcq.py tests/multiplechoice_question.tex
```

Import the generated XML files into Moodle and check that:

- The description heading and text display correctly.
- Mathematics displays correctly in the description, question, and choices.
- The correct answer is recognised.
- The text inside `solutionorbox` does not appear.

`tests/latex_preview.tex` provides a LaTeX preview.