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

For batches, give related supported LaTeX files a common filename prefix. For example, `01_logic_description.tex` and `01_logic_question1.tex` share the prefix `01_logic`. If these files are stored directly in the project folder, use:

```bash
python3 main.py 01_logic
```

This produces `01_logic2moodle.xml`. To run batch conversion without a filename prefix and produce `2moodle.xml`, use an empty prefix:

```bash
python3 main.py ""
```

For a prefix, the program:

1. Converts matching supported LaTeX files in filename order, choosing description or multiple-choice conversion for each.
2. Merges matching Moodle XML files into `<prefix>2moodle.xml`.
3. Deletes the individual XML files after the merged output is written successfully.

Prefixes are literal filename prefixes; `""` matches every filename. Subfolders are not searched. Every selected `.tex` file must be a supported LaTeX file: selection checks filenames, not contents.

Batch conversion skips filenames ending in `_chatgpt` before `.tex`, regardless of capitalisation. For example, `01_logic_ChatGPT.tex` and `01_logic_CHATGPT.tex` are excluded, including when the prefix is empty. A supported LaTeX file supplied explicitly is still converted.

Existing matching XML files are also merged and deleted, including files such as `01_logic_ChatGPT.xml`: the exclusion applies only to selecting LaTeX files. The merged output itself is excluded from the inputs and replaced on each successful run. The LaTeX source files are retained. If conversion or merging fails, cleanup does not run.

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

## Run from any folder on Linux

These instructions make the `tex2moodle` command available to your Linux user account in Bash terminals.

From the project folder, run `pwd` to find its full path. Replace `/absolute/path/to/tex2moodle` below with that path, then run these commands to create the launcher:

```bash
mkdir -p "$HOME/.local/bin"

cat > "$HOME/.local/bin/tex2moodle" <<'EOF'
#!/bin/sh
exec python3 "/absolute/path/to/tex2moodle/main.py" "$@"
EOF

chmod +x "$HOME/.local/bin/tex2moodle"
```

Open `~/.bashrc` in a text editor and add this line if it is not already present. This tells Bash where to find the launcher:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Save `~/.bashrc`, then reload it in your terminal and check the command:

```bash
source "$HOME/.bashrc"
command -v tex2moodle
tex2moodle --help
```

`command -v` should print the path to `~/.local/bin/tex2moodle`. The setting persists in new Bash terminals.

To use the installed command, open a terminal in the folder containing your supported LaTeX files:

```bash
tex2moodle question.tex  # Convert one supported LaTeX file
tex2moodle 01_logic      # Convert and merge files with this prefix
tex2moodle ""            # Batch conversion without a prefix, applying the exclusions above
```

Replace `question.tex` or `01_logic` with your filename or prefix. Output files are saved in the same folder, following the conversion and deletion rules above.
