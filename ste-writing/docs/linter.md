# ste_lint.py reference

`scripts/ste_lint.py` checks technical text against the rules in `SKILL.md`.
The default mode matches STE-flavored. The `--strict` option matches strict
mode and adds checks against the full STE100 dictionary. The script needs
only the Python standard library.

## Usage

```bash
python3 scripts/ste_lint.py FILE [FILE ...]   # STE-flavored checks
python3 scripts/ste_lint.py --strict FILE     # strict, adds dictionary checks
python3 scripts/ste_lint.py --format json FILE
python3 scripts/ste_lint.py --ignore W01,V01 FILE
python3 scripts/ste_lint.py < FILE            # reads standard input
```

- The exit code is 1 when a finding has the severity error, and 0 otherwise.
- `--ignore` takes a comma-separated list of rule ids.
- `--format json` prints the findings as one JSON array.
- `NO_COLOR=1` turns off the colored output.
- Put examples of banned words in backticks: the linter skips code spans.

## Input handling

- The linter skips fenced code blocks, inline code, YAML frontmatter, tables, and block quotes.
- It joins the lines of a paragraph, then splits the text into sentences.
- The sentence splitter protects common abbreviations such as `e.g.`
- A heading joins the next paragraph when no blank line comes after it.

## Rule reference

| Id | Mode | Severity | What it flags | Data source |
|----|------|----------|---------------|-------------|
| P01 | both | error | em dash, en dash | fixed pattern |
| W01 | both | error | a word from the preferred-word list, with inflections | `SKILL_BANNED` |
| W02 | both | error | a contraction, but not a noun possessive | `CONTRACTION_RE` |
| W03 | both | error | a marketing adjective | `MARKETING` |
| W04 | both | error | an AI-slop phrase | `SLOP_PHRASES` |
| V01 | both | warning | a form of `be` plus a past participle | participles from the dictionary |
| V02 | both | warning | a nominalization, for example `perform an analysis` | `NOMINALIZATION_RE` |
| V03 | both | warning | stacked auxiliaries, for example `helps to` | `AUX_CHAIN_RE` |
| V04 | both | warning | a step that starts with an -ing form | fixed pattern |
| S01 | both | error | a sentence over 20 words (instruction) or 25 words (descriptive) | `MAX_INSTR`, `MAX_DESCR` |
| S02 | both | warning | a paragraph over six sentences | fixed cap |
| S03 | both | warning | a list item with two sentences or `and then` | fixed pattern |
| S04 | both | warning | a condition after the command in a step | fixed pattern |
| D01 | strict | error | a word that STE100 does not approve | `not_approved` map |
| D02 | strict | info | a word that occurs in neither map of the dictionary | `approved` map |
| D03 | strict | info | a word with mixed status across parts of speech | both maps |

## Pipeline

1. `Doc` splits the file into units: paragraphs and list items.
2. `check_words` applies P01, W01 to W04, and the strict D-rules to each unit.
3. `check_units` splits each unit into sentences and applies V01 to V04 and S01 to S04.
4. The report shows each finding as `file:line:column: severity rule: message`.

## Heuristics and limits

- V01, V04, S04, and the imperative detection of S01 are heuristics and can give false positives.
- V01 matches a form of `be` with a participle from the approved-verb list.
- The linter counts a hyphenated compound as one word.
- The linter matches words without part-of-speech tagging: read a D01 message together with the headword part of speech.

## Customization points

- Edit `SKILL_BANNED`, `MARKETING`, or `SLOP_PHRASES` to change the word lists.
- Edit `MAX_INSTR` and `MAX_DESCR` to change the sentence caps.
- Add a `check_*` method for a new rule family, and call it from `lint_text`.
- Change the severity argument of `self.add` to move a rule between error, warning, and info.
- The D-rules read only `ste_dictionary.json`: change the data file, not the code.
- The dictionary also feeds V01 and S01 in both modes: refer to `references/dictionary.md`.
