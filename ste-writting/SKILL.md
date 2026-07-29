---
name: ste-writing
description: skill of writing technical documents (docs, manuals, README, PR descriptions, error messages, release notes, comments of code) in ASD-STE100 Simplified Technical English to remove "AI slop". Use whenever you write technical documents or be asked to make writing not sound like AI, make docs clear, concise, or plain, enforce a controlled writing style. Two modes: strict and STE-flavored.
---

## Overview

Writing in ASD-STE100 Simplified Technical English. This applies to documents, manuals, README, pull-request text, error messages, release notes, and comments of code. It does not apply to code itself. It is not for articles, essays, or anything that needs an argument.

In general, make technical text concise and clear, mechanically checkable with rules and the linter in scripts/.

## Rules

WORDS
- Use one name for one thing. Do not call the same thing by two different names. Do not write synonyms separated by '/' or with '()'. 
- Use the short common word. For example, start (not begin/commence/initiate), use (not utilize/leverage), help (not facilitate), make sure (not ensure), before (not prior to), after (not subsequent to), about (not regarding/concerning), get (not obtain/acquire), show (not demonstrate), also (not additionally/furthermore/moreover).
- Give each word one meaning. For example, "fall" means to move down, not to decrease. Do not use both exchangeably.
- No marketing adjectives. For example, seamless, robust, powerful, cutting-edge, effortless, world-class, next-generation, revolutionary.
- No contractions.
- Use articles: a, an, the, this, these.

VERBS
- Active voice. "the parser reads the file", not "the file is read by the parser".
- Use a verb for an action. "analyze the log", not "perform an analysis of the log".
- No stacked auxiliaries. Not "it is important to note that this may help to improve". Write "this improves X".
- No "-ing" main verb where a simple tense works.

SENTENCES
- One instruction per sentence. Max 20 words (instruction), max 25 (descriptive).

PUNCTUATION
- No em dash. Write two sentences. 

STRUCTURE
- One topic per paragraph, max six sentences. For steps, use a numbered vertical list, one action per item, imperative form. Put a condition before its command.

## Modes

- **strict**: procedures, runbooks, safety text, error messages: apply every rule and both length caps. Only approved words plus your project's technical nouns and verbs.
- **STE-flavored**: general prose (READMEs, PR descriptions, docs): apply the sentence, paragraph, and active-voice rules and the banned-word lists. Relax the approved-dictionary lockdown so the text keeps enough range to read naturally.

## Validation

1. Write only the requested text. No preamble, no summary, no closing remarks.

2. After you write or edit text, run the linter for the applicable mode:

```bash
python scripts/ste_lint.py <file>            # STE-flavored
python scripts/ste_lint.py --strict <file>   # strict
```

3. Fix every error. Check warnings one by one: passive voice (V01) and condition order (S04) are heuristics, confirm before you change the text.
4. Run the linter again until it reports no errors. Use `--ignore <rule ids>` only when a rule does not apply to the document type.

Rule ids: P01 em dash; W01 banned word (list above); W02 contraction; W03 marketing adjective; W04 AI-slop phrase; V01 passive voice; V02 nominalization; V03 stacked auxiliaries; V04 -ing step; S01 length cap; S02 paragraph over six sentences; S03 several actions per item; S04 condition after command. Strict mode adds: D01 word not approved in the STE100 dictionary; D02 word not in the approved dictionary; D03 word approved only as a different part of speech or with restricted meanings.

D01-D03 come from the full STE100 dictionary (scripts/ste_dictionary.json, 875 approved and 1274 not-approved words, extracted from Issue 9 with scripts/extract_dictionary.py). A D01-D03 finding can still be correct when the word is a technical noun or technical verb approved by your project (STE100 rules 1.5 and 1.12). Keep it then, and do not "fix" it.

Read references/linter.md for the full rule reference, the pipeline, and the customization points. Read references/dictionary.md for the dictionary format, regeneration, and project customization. The full specification is at references/ASD-STE100_ISSUE9.pdf.

