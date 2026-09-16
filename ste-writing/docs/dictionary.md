# ste_dictionary.json reference

`scripts/ste_dictionary.json` holds the dictionary of ASD-STE100, part 2 of
the specification. `scripts/extract_dictionary.py` read the Issue 9 PDF with
`pdftotext -layout` and wrote this file. The file has two maps: `approved`
and `not_approved`.

The `approved` map has 801 words, or 874 entries with parts of speech. The
`not_approved` map has 1243 words with their approved alternatives. The
specification counts 875 approved entries and more than 1274 not-approved
words: the difference is extraction noise.

## Format of an approved entry

```json
"ACCEPT": {
  "pos": ["v"],
  "sentences": [2],
  "forms": ["ACCEPTS", "ACCEPTED", "ACCEPTED"],
  "meanings": ["To take or receive something that is given."]
}
```

- `pos`: the approved parts of speech.
- `sentences`: numbers of the example sentences in the specification.
- `forms`: the approved inflections.
- `meanings`: the approved meanings, in the wording of the specification.

## Format of a not-approved entry

```json
"begin": {
  "pos": ["v"],
  "sentences": [23],
  "alternatives": ["START (v)"],
  "notes": []
}
```

- `alternatives`: the approved replacements from the specification.
- `notes`: other guidance, such as "Use an accurate verb."

## How the linter uses the maps

- D01 flags each inflected form of a not-approved word and shows the alternatives.
- D02 flags a word that occurs in neither map.
- D03 flags a word with mixed status: approved as one part of speech, not approved as another.
- Inflected forms of approved nouns also count as approved: the specification permits plural forms.
- Approved verbs feed two more checks: the imperative detection of S01 and the participle list of V01.

## Regeneration

```bash
python3 scripts/extract_dictionary.py references/ASD-STE100_ISSUE9.pdf scripts/ste_dictionary.json
```

- The script needs `pdftotext` from poppler.
- The source PDF is at `references/ASD-STE100_ISSUE9.pdf`.
- The script reproduces the shipped file exactly.

## Customization for software documentation

Some not-approved words are common in software text, for example `run` (v),
`serve` (v), and `reduce` (v). Two mechanisms already exist for project
words: technical nouns (rule 1.5) and technical verbs (rule 1.12). D02 info
findings mark candidates for your project glossary.

When your project accepts a word, change the dictionary:

1. Open `scripts/ste_dictionary.json`.
2. Delete the entry from `not_approved`, or move the entry to `approved`.
3. When you add an approved verb, fill `pos` and `forms`.
4. Run the linter on a sample file to check the change.
5. Record each change in a project note: regeneration from the PDF overwrites local edits.

Example entry for `run` as an approved technical verb:

```json
"RUN": {
  "pos": ["v", "TV"],
  "sentences": [],
  "forms": ["RUNS", "RUNNING", "RAN"],
  "meanings": ["To operate. (project addition)"]
}
```

Note: the participle list of V01 comes from forms that end in `ed`. A new
approved verb adds no participle: add the `ed` form to `forms` for passive
detection.

## Known extraction noise

- A few alternatives hold fragments from example sentences: a layout artifact of the PDF.
- Some not-approved entries have no alternatives: the linter shows the note instead.
- The parser joined wrapped lines by column position: check odd entries against the PDF.
