# tex2moodle

tex2moodle converts supported LaTeX files into Moodle XML for importing descriptions and single-answer multiple-choice questions into a Moodle question bank.

## Usage

Open a terminal in the project folder, which contains `main.py`. Run the following commands from there.

To convert the supplied supported LaTeX files individually:

```bash
python3 main.py tests/supported_description.tex
python3 main.py tests/supported_multiplechoice_question.tex
```

An argument ending in `.tex` converts one supported LaTeX file and keeps its individual `.xml` output beside it. An existing output with the same name is overwritten.

For batches, give related supported LaTeX files a common filename prefix. For example, `supported_description.tex` and `supported_multiplechoice_question.tex` share the prefix `supported`. If these files are stored directly in the project folder, use:

```bash
python3 main.py supported
```

This produces `supported2moodle.xml`. To run batch conversion without a filename prefix and produce `2moodle.xml`, use an empty prefix:

```bash
python3 main.py ""
```

For a prefix, the program:

1. Converts matching supported LaTeX files in filename order, choosing description or multiple-choice conversion for each.
2. Merges matching Moodle XML files into `<prefix>2moodle.xml`.
3. Deletes the individual XML files after the merged output is written successfully.

Prefixes are literal filename prefixes; `""` matches every filename. Subfolders are not searched. Every selected `.tex` file must be a supported LaTeX file: selection checks filenames, not contents.

Batch conversion skips filenames ending in `_chatgpt` before `.tex`, regardless of capitalisation. For example, `supported_multiplechoice_question_ChatGPT.tex` and `supported_multiplechoice_question_CHATGPT.tex` are excluded, including when the prefix is empty. A supported LaTeX file supplied explicitly is still converted.

Existing matching XML files are also merged and deleted. The merged output itself is excluded from the inputs and replaced on each successful run. The LaTeX source files are retained. If conversion or merging fails, cleanup does not run.

## Supported LaTeX files

Use the [description example](tests/supported_description.tex) and [multiple-choice example](tests/supported_multiplechoice_question.tex) as templates for your own supported LaTeX files.

- **Descriptions:** filenames containing `description` become Moodle descriptions.
- **Multiple-choice questions:** files with other names must contain one `\question` followed by a `mychoices` environment. Mark one answer with `\CorrectChoice` and the remaining answers with `\choice`.

Supported content includes:

- Simple `\subsection*{...}` headings, converted to HTML headings.
- Inline maths written as `$...$`, converted to `\(...\)` with missing spaces added around unescaped `<`, `>` and `&` inside maths.
- Simple unnumbered (`itemize`) and numbered (`enumerate`) lists, converted to HTML lists.

Nested lists, custom list labels/options, display maths and `\input` expansion are unsupported. `tests/latex_preview.tex` relies on `\input` and is not a supported LaTeX file for conversion; exclude it from batches.

## Check the output

Import the generated XML into Moodle. Check that headings, maths and lists display correctly, the correct answer is recognised, and the text inside `solutionorbox` is absent. `tests/latex_preview.pdf` shows the LaTeX examples for comparison.
