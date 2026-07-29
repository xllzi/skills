---
name: ste-writing
description: skill of writting technical documents (docs, manuals, README, PR descriptions, error messages, release notes, comments of code) in ASD-STE100 Simplified Technical English to remove "AI slop". Use whenever you write technical documents or be asked to make writing not sound like AI, make docs clear ,concise or plain, enforce a controlled writing style. Two modes — strict and STE-flavored.
---

## Overview

Writing in ASD-STE100 Simplified Technical English. This applies to documents, manuals, README, pull-request text, error messages, release notes, and comments of code. It does not apply to code itself. It is not for aritcles, essays, or anything that needs a argument.

In general, make technical text concise and clear, mechanical checkable by following rules.

## Rules

WORDS
- Use one name for one thing. Do not call the same thing by two different names. Do not write synonyms in the context seperated by '/' or with '()'. 
- Use the short common word. For example, start (not begin/commence/initiate), use (not utilize/leverage), help (not facilitate), make sure (not ensure), before (not prior to), after (not subsequent to), about (not regarding/concerning), get (not obtain/acquire), show (not demonstrate), also (not additionally/furthermore/moreover).
- Give each word one meaning. For example, "fall" means to move down, not to decrease. Do not use both exchangably.
- No marketing adjectives. For example, seamless, robust, powerful, cutting-edge, effortless, world-class, next-generation, revolutionary.
- No contractions only. Ethier expand it or add full name in '()'
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

Write only the requested text. No preamble, no summary, no closing remarks.

## Modes

- **strict** — procedures, runbooks, safety text, error messages: apply every rule and both length caps.
- **STE-flavored** — general prose (READMEs, PR descriptions, docs): apply the sentence, paragraph, active-voice, and no-phrasal-verb discipline; relax the ~900-word dictionary lockdown so the text keeps enough range to read naturally.

