# tex2moodle

Convert LaTeX descriptions and single-answer multiple-choice questions into a Moodle XML question bank.

You need Python 3. No extra Python packages are required. Start with the supplied examples, then use them as templates for your own questions.

## Convert one file

Open a terminal in the project folder—the folder containing `main.py`—and run:

```bash
python3 main.py tests/supported_description.tex
python3 main.py tests/supported_multiplechoice_question.tex
```

These commands create `tests/supported_description.xml` and `tests/supported_multiplechoice_question.xml`. You can import either file into Moodle.

Each XML file is saved beside its LaTeX source. An existing XML file with the same name is replaced. The LaTeX source is kept.

**Wrong answers receive zero by default.** Add `--penalty` if you want negative grades for wrong answers.

## Convert several files at once

Give related LaTeX files a shared filename prefix. For example, `supported_description.tex` and `supported_multiplechoice_question.tex` both start with `supported`.

If those files are beside `main.py`, run:

```bash
python3 main.py supported
```

This creates one file: `supported2moodle.xml`.

**Batch conversion searches the folder where you run the command. It does not search subfolders.** To convert the supplied examples, which are in `tests/`, run these commands from the project folder:

```bash
cd tests
python3 ../main.py supported
cd ..
```

The result is `tests/supported2moodle.xml`. The last command returns you to the project folder.

To select every eligible `.tex` file beside `main.py`, use an empty prefix:

```bash
python3 main.py ""
```

This creates `2moodle.xml`. Every selected file must follow the supported format below; files are selected by name, not by their contents.

### Which files are included?

A prefix matches the start of a filename exactly. Batch conversion skips names ending in `_chatgpt` before `.tex`, in any mix of upper and lower case. This rule also applies to an empty prefix. If you pass one of those files explicitly, it is converted.

### What happens to the files?

A batch run:

1. Converts matching LaTeX files in filename order.
2. Combines matching XML files into `<prefix>2moodle.xml`.
3. Deletes the individual XML files after the combined file is saved successfully.

**Existing XML files that match the prefix are also included and deleted.** The combined output is excluded from its own inputs and replaced on each successful run. LaTeX sources are kept. If conversion or merging fails, the deletion step does not run.

## Choose whether wrong answers carry a penalty

Add `--penalty` to a single-file command:

```bash
python3 main.py tests/supported_multiplechoice_question.tex --penalty
```

Or add it to a batch command. With the source files beside `main.py`:

```bash
python3 main.py supported --penalty
```

Omit the flag for no penalty. The flag takes no value and applies to every multiple-choice question converted in that run.

| Setting | Correct answer | Each wrong answer |
| --- | --- | --- |
| No flag | 100% | 0% |
| `--penalty` | 100% | −100% divided by the total number of choices |

For a question with four choices, including the correct choice, `--penalty` gives each wrong answer a grade of **−25%**. Without the flag, each wrong answer gets **0%**. These are the answer grades written to the Moodle XML.

Descriptions are unaffected. XML files merged without being regenerated keep their existing grades.

## Prepare your LaTeX files

Use UTF-8 text and a `.tex` extension.

**Input `.tex` files are expected to contain no LaTeX comments.** This includes full-line and trailing comments introduced by an unescaped `%`.

If a possible comment is detected, the converter prints a warning naming the file and continues. It does not remove comments, so they may appear in the XML or interfere with question and answer parsing.

Start with these templates:

- [Description](tests/supported_description.tex): a filename containing lowercase `description` creates a Moodle description.
- [Multiple-choice question](tests/supported_multiplechoice_question.tex): other filenames create multiple-choice questions. Each file must contain one `\question` followed by a `mychoices` environment. Mark one answer with `\CorrectChoice` and the others with `\choice`.

The converter supports:

- Headings written as `\subsection*{...}`.
- Bold and italic text written as `\textbf{...}` and `\textit{...}`.
- Inline maths written as `$...$`, converted to `\(...\)`.
- Unnumbered display equations in `\begin{equation*}...\end{equation*}`, converted to `\[...\]`.
- Simple bulleted (`itemize`) and numbered (`enumerate`) lists.

Headings and text formatting must use simple contents without nested braces. Nested lists, custom list labels or options, and `\input` expansion are unsupported. Other display-maths environments are not converted.

The file [latex_preview.tex](tests/latex_preview.tex) uses `\input` to assemble the examples for printing. It cannot be converted to Moodle XML. Use the `supported` prefix when converting the contents of `tests/`; an empty prefix would also select this preview file.

## Check the result in Moodle

Import the output into your question bank using the Moodle XML format. Preview the questions and check the formatting, maths, correct answer, and answer grades.

The [PDF preview](tests/latex_preview.pdf) shows the original LaTeX examples for comparison. In the converted multiple-choice question, the text inside `solutionorbox` should be absent.
