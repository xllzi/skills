#!/usr/bin/env python3
"""Lint technical text against the distilled ASD-STE100 rules in SKILL.md.

Checks word choice, voice, sentence and paragraph length, and punctuation.
Word-level checks use the official STE100 dictionary data in
ste_dictionary.json (extracted from ASD-STE100 Issue 9).

Modes:
  flavored (default): the skill's core discipline - banned-word list from
      SKILL.md, marketing adjectives, contractions, em dashes, active voice,
      sentence/paragraph caps.
  strict: everything above, plus the full STE100 non-approved word list
      and an info-level report of words that are not in the approved
      dictionary (allowed only as technical nouns/verbs, rules 1.5/1.12).

Exit code: 1 if any error-severity finding, else 0.
"""
import argparse
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DICT_PATH = os.path.join(SCRIPT_DIR, "ste_dictionary.json")

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_dictionary(path=DICT_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def inflections(word):
    """Plausible surface forms of a base word (lowercase)."""
    out = {word, word + "s", word + "es", word + "d", word + "ed",
           word + "ing", word + "ly", word + "er", word + "est"}
    if word.endswith("e"):
        out.update({word[:-1] + "ing", word + "r", word + "st"})
    if word.endswith("y") and len(word) > 1 and word[-2] not in "aeiou":
        out.update({word[:-1] + "ies", word[:-1] + "ied", word[:-1] + "ily"})
    if len(word) > 2 and word[-1] not in "aeiouwy" and word[-2] in "aeiou" \
            and word[-3] not in "aeiou":
        out.update({word + word[-1] + "ing", word + word[-1] + "ed"})
    return out


class Dict:
    def __init__(self, data):
        ok = data["approved"]
        self.approved_vocab = set()
        self.approved_pos = {}        # word -> approved parts of speech
        self.approved_verbs = set()   # base forms + inflections, for imperatives
        self.participles = set()      # past participles, for passive detection
        for word, ent in ok.items():
            w = word.lower()
            self.approved_vocab.add(w)
            self.approved_pos.setdefault(w, set()).update(ent["pos"])
            for f in ent["forms"]:
                f = f.lower()
                self.approved_vocab.add(f)
                self.approved_pos.setdefault(f, set()).update(ent["pos"])
            if "n" in ent["pos"]:  # plurals of countable nouns are permitted
                for f in inflections(w):
                    self.approved_vocab.add(f)
                    self.approved_pos.setdefault(f, set()).add("n")
            if "v" in ent["pos"]:
                self.approved_verbs.add(w)
                self.approved_verbs.update(f.lower() for f in ent["forms"])
                for f in ent["forms"]:
                    f = f.lower()
                    if f.endswith("ed") or f in IRREG_PARTICIPLES:
                        self.participles.add(f)
        self.participles |= IRREG_PARTICIPLES
        # not-approved word -> (pos list, suggestion text, note)
        self.banned = {}
        for word, ent in data["not_approved"].items():
            alts = list(dict.fromkeys(ent.get("alternatives") or []))
            sug = "; ".join(alts[:3])
            note = " ".join(ent.get("notes", []))
            self.banned[word] = (ent.get("pos", []), sug, note)
        # surface form -> base headword (for inflected lookups)
        self.banned_forms = {}
        for word in self.banned:
            if " " in word:
                continue
            for form in inflections(word):
                self.banned_forms.setdefault(form, word)
        # multi-word banned phrases: first word -> [(words, headword)]
        self.banned_phrases = {}
        for word in self.banned:
            if " " in word:
                parts = word.split()
                self.banned_phrases.setdefault(parts[0], []).append(
                    (parts, word))


IRREG_PARTICIPLES = {
    "been", "done", "gone", "made", "known", "given", "taken", "seen",
    "written", "read", "built", "set", "cut", "shut", "sent", "left",
    "lost", "found", "held", "told", "sold", "brought", "thought",
    "bought", "caught", "taught", "chosen", "driven", "fallen",
    "forgotten", "frozen", "grown", "hidden", "kept", "led", "met",
    "paid", "said", "shown", "spoken", "stolen", "swept", "swum",
    "torn", "thrown", "understood", "worn", "won", "got", "gotten",
    "broken", "eaten", "risen", "blown", "drawn", "flown", "laid",
}

# ---------------------------------------------------------------------------
# Rule data from SKILL.md
# ---------------------------------------------------------------------------

# "Use the short common word" list (WORDS rule). Verified against the
# STE100 dictionary where the word has an entry there.
SKILL_BANNED = {
    "begin": "start", "commence": "start", "initiate": "start",
    "utilize": "use", "leverage": "use",
    "facilitate": "help",
    "ensure": "make sure",
    "prior to": "before",
    "subsequent to": "after",
    "regarding": "about", "concerning": "about",
    "obtain": "get", "acquire": "get",
    "demonstrate": "show",
    "additionally": "also", "furthermore": "also", "moreover": "also",
}

MARKETING_ADJ = [
    "seamless", "seamlessly", "robust", "powerful", "cutting-edge",
    "effortless", "effortlessly", "world-class", "next-generation",
    "revolutionary",
]

# Common AI-slop phrasing. Aligned with the skill's purpose and the
# "no stacked auxiliaries" rule.
SLOP_PHRASES = {
    "it is important to note": "delete, or state the fact directly",
    "it's important to note": "delete, or state the fact directly",
    "please note that": "delete, or write NOTE:",
    "in order to": "to",
    "due to the fact that": "because",
    "delve": "examine",
    "firstly": "first", "secondly": "second", "thirdly": "third",
}

CONTRACTION_RE = re.compile(
    r"\b\w+(n't|''re|''ve|''ll|''d|''m|'re|'ve|'ll|'d|'m)\b|"
    r"\b(it's|that's|there's|here's|what's|let's|he's|she's|who's|how's)\b",
    re.IGNORECASE)

EMDASH_RE = re.compile(r"—|–|&#8212;|&#8211;|&mdash;|&ndash;|\s--\s")

PASSIVE_RE = None  # built from dictionary participles

NOMINAL_RE = re.compile(
    r"\b(perform|conduct|make|carry out|do)\s+(?:a|an|the|some)?\s*"
    r"(\w*(?:tion|sion|ment|ance|ence|sis))\b", re.IGNORECASE)

STACKED_RE = re.compile(
    r"\b(may|might|could|can)\s+(?:also\s+)?helps?\s+to\b|"
    r"\bhelps?\s+to\s+\w+|"
    r"\bit is important to\b|"
    r"\ballows?\s+(?:you\s+)?to\b|"
    r"\benables?\s+(?:you\s+)?to\b", re.IGNORECASE)

CONDITION_WORDS = ("if", "when", "before", "after", "unless", "until")

# ---------------------------------------------------------------------------
# Markdown / text preprocessing
# ---------------------------------------------------------------------------

FENCE_RE = re.compile(r"^\s*(```|~~~)")
ORDERED_RE = re.compile(r"^(\s*)\d+[.)]\s+")
UNORDERED_RE = re.compile(r"^\s*[-*+]\s+")
HEADING_RE = re.compile(r"^\s*#{1,6}\s")
TABLE_RE = re.compile(r"^\s*\|")


def strip_inline(text):
    text = re.sub(r"`[^`]*`", " ", text)                 # inline code
    text = re.sub(r"<!--.*?-->", " ", text)             # html comments
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)   # images
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links
    text = re.sub(r"https?://\S+", " ", text)           # bare urls
    text = re.sub(r"[*_]{1,3}([^*_]+)[*_]{1,3}", r"\1", text)  # emphasis
    return text


class Doc:
    """Source split into checkable units with line numbers."""

    def __init__(self, text):
        self.lines = text.splitlines()
        self.units = []        # (line_no, kind, text)
        self.prose_lines = []  # (line_no, cleaned_text) for word checks
        in_fence = False
        para = []              # accumulated paragraph (list of (line, text))
        start = 0
        if self.lines and self.lines[0].strip() == "---":  # yaml frontmatter
            for i, ln in enumerate(self.lines[1:], 1):
                if ln.strip() in ("---", "..."):
                    start = i + 1
                    break
        for n, raw in enumerate(self.lines[start:], start + 1):
            if FENCE_RE.match(raw):
                if in_fence:
                    in_fence = False
                    self._flush_para(para)
                    para = []
                    continue
                in_fence = True
                self._flush_para(para)
                para = []
                continue
            if in_fence:
                continue
            line = raw.strip()
            if not line:
                self._flush_para(para)
                para = []
                continue
            if HEADING_RE.match(raw):
                self._flush_para(para)
                para = []
                cleaned = strip_inline(line.lstrip("#").strip())
                self.units.append((n, "heading", cleaned))
                self.prose_lines.append((n, cleaned))
                continue
            m = ORDERED_RE.match(raw)
            if m:
                self._flush_para(para)
                para = []
                cleaned = strip_inline(raw[m.end():].strip())
                self.units.append((n, "step", cleaned))
                self.prose_lines.append((n, cleaned))
                continue
            if UNORDERED_RE.match(raw):
                self._flush_para(para)
                para = []
                cleaned = strip_inline(re.sub(r"^\s*[-*+]\s+", "", raw).strip())
                self.units.append((n, "bullet", cleaned))
                self.prose_lines.append((n, cleaned))
                continue
            if TABLE_RE.match(raw):
                self._flush_para(para)
                para = []
                cleaned = strip_inline(line)
                self.prose_lines.append((n, cleaned))
                continue
            cleaned = strip_inline(line.lstrip(">").strip())
            para.append((n, cleaned))
            self.prose_lines.append((n, cleaned))
        self._flush_para(para)

    def _flush_para(self, para):
        if para:
            self.units.append((para[0][0], "para", list(para)))


ABBR_RE = re.compile(r"\b(e\.g|i\.e|etc|Fig|fig|No|no|vs|approx)\.")
DOTTED_RE = re.compile(r"(\d)\.(\d)")  # 1.2 version numbers


def split_sentences(text):
    t = ABBR_RE.sub(lambda m: m.group(1) + "\x00", text)
    t = DOTTED_RE.sub(lambda m: m.group(1) + "\x00" + m.group(2), t)
    parts = re.split(r"(?<=[.!?])\s+", t)
    return [p.replace("\x00", ".").strip() for p in parts
            if p.replace("\x00", ".").strip()]


def count_words(sentence):
    return len([t for t in re.findall(r"\S+", sentence)
                if re.search(r"[A-Za-z0-9]", t)])


# ---------------------------------------------------------------------------
# Linter
# ---------------------------------------------------------------------------

class Linter:
    def __init__(self, data, strict=False, ignore=frozenset()):
        self.d = Dict(data)
        self.strict = strict
        self.ignore = ignore
        self.findings = []
        self.passive_re = re.compile(
            r"\b(is|are|was|were|be|been|being|get|gets|got|gotten|getting)"
            r"\s+(?:\w+ly\s+)?(" + "|".join(
                sorted(self.d.participles, key=len, reverse=True)) + r")\b",
            re.IGNORECASE)

    def add(self, file, line, col, rule, sev, msg):
        if rule not in self.ignore:
            self.findings.append(
                {"file": file, "line": line, "col": col, "rule": rule,
                 "severity": sev, "message": msg})

    # -- word-level checks -------------------------------------------------

    def check_words(self, file, line_no, text):
        d = self.d
        for m in EMDASH_RE.finditer(text):
            self.add(file, line_no, m.start() + 1, "P01", "error",
                     "em/en dash: write two sentences (PUNCTUATION rule)")
        m = CONTRACTION_RE.search(text)
        if m:
            self.add(file, line_no, m.start() + 1, "W02", "error",
                     f"contraction {m.group(0)!r}: write the full form "
                     "(WORDS rule)")
        tokens = [(m.group(0), m.start())
                  for m in re.finditer(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", text)]
        low = [t[0].lower() for t in tokens]
        for i, (tok, col) in enumerate(tokens):
            lw = low[i]
            bare = lw.split("'")[0]
            # marketing adjectives
            if lw in MARKETING_ADJ or bare in MARKETING_ADJ:
                self.add(file, line_no, col + 1, "W03", "error",
                         f"marketing adjective {tok!r}: use a measurable "
                         "fact (WORDS rule)")
                continue
            # AI-slop single words
            if lw in ("delve", "delves", "delved", "delving"):
                self.add(file, line_no, col + 1, "W04", "error",
                         f"{tok!r}: use 'examine' (de-AI-slop)")
                continue
            # skill banned list (both modes)
            hit = self._lookup(SKILL_BANNED, low, i)
            if hit:
                head, sug = hit
                self.add(file, line_no, col + 1, "W01", "error",
                         f"{head!r}: use {sug!r} (WORDS rule)")
                continue
            # full STE100 dictionary (strict mode)
            if self.strict:
                if lw in d.banned_forms:
                    head = d.banned_forms[lw]
                    pos, sug, note = d.banned[head]
                    if lw in d.approved_vocab:
                        ok_pos = d.approved_pos.get(lw, set())
                        if ok_pos & set(pos):
                            msg = (f"{tok!r}: approved only with its "
                                   "approved meanings (rule 1.3)")
                        else:
                            msg = (f"{tok!r}: approved only as "
                                   f"({'/'.join(sorted(ok_pos))}); do not "
                                   f"use as ({'/'.join(pos)})")
                        if sug:
                            msg += f": {sug}"
                        self.add(file, line_no, col + 1, "D03", "info", msg)
                    else:
                        msg = (f"{head!r} ({'/'.join(pos)}) is not "
                               "approved in STE100")
                        if sug:
                            msg += f": use {sug}"
                        elif note:
                            msg += f": {note[:100]}"
                        self.add(file, line_no, col + 1, "D01", "error",
                                 msg)
                    continue
                for first, phrases in d.banned_phrases.items():
                    if lw != first:
                        continue
                    for parts, head in phrases:
                        n = len(parts)
                        if low[i:i + n - 1] == parts[:-1] and i + n <= len(low)\
                                and low[i + n - 1] in inflections(parts[-1]):
                            pos, sug, note = d.banned[head]
                            msg = (f"{head!r} ({'/'.join(pos)}) is not "
                                   "approved in STE100")
                            if sug:
                                msg += f": use {sug}"
                            self.add(file, line_no, col + 1, "D01", "error",
                                     msg)
            # lockdown: word not in approved vocabulary (strict, info)
            if self.strict and len(lw) > 2 and lw.isalpha() \
                    and not tok.isupper() and lw not in d.approved_vocab:
                self.add(file, line_no, col + 1, "D02", "info",
                         f"{tok!r} is not in the STE100 dictionary: allowed "
                         "only as an approved technical noun/verb "
                         "(rules 1.5, 1.12)")
        # slop phrases
        textlow = " " + text.lower() + " "
        for phrase, sug in SLOP_PHRASES.items():
            idx = textlow.find(phrase)
            if idx >= 0:
                self.add(file, line_no, idx, "W04", "error",
                         f"{phrase!r}: {sug} (de-AI-slop)")

    def _lookup(self, mapping, low, i):
        """Match single words (with inflections) and phrases in `mapping`."""
        lw = low[i]
        for head, sug in mapping.items():
            if " " not in head and lw in inflections(head):
                return head, sug
        for head, sug in mapping.items():
            if " " in head:
                parts = head.split()
                n = len(parts)
                if low[i:i + n - 1] == parts[:-1] and i + n <= len(low) \
                        and low[i + n - 1] in inflections(parts[-1]):
                    return head, sug
        return None

    # -- sentence / structure checks ----------------------------------------

    def check_units(self, file, doc):
        for unit in doc.units:
            kind = unit[1]
            if kind == "para":
                self._check_para(file, unit)
            elif kind == "step":
                self._check_step(file, unit)
            elif kind in ("bullet", "heading"):
                self._check_sentence_caps(file, unit[0], unit[2],
                                          instruction=False)

    def _check_para(self, file, unit):
        line_no, _, para = unit
        full = " ".join(t for _, t in para)
        sentences = split_sentences(full)
        if len(sentences) > 6:
            self.add(file, line_no, 1, "S02", "warning",
                     f"paragraph has {len(sentences)} sentences "
                     "(max 6, STRUCTURE rule)")
        cursor = 0
        for s in sentences:
            start_line = para[0][0]
            acc = 0
            for ln, t in para:
                idx = full.find(s, cursor)
                if idx >= acc + len(t):
                    acc += len(t) + 1
                    continue
                start_line = ln
                break
            cursor = full.find(s, cursor) + len(s)
            self._check_sentence_caps(file, start_line, s,
                                      instruction=self._is_imperative(s))

    def _check_step(self, file, unit):
        line_no, _, text = unit
        sentences = split_sentences(text)
        if len(sentences) > 1:
            self.add(file, line_no, 1, "S03", "warning",
                     f"list item has {len(sentences)} sentences: "
                     "one action per item (STRUCTURE rule)")
        if " and then " in text.lower():
            self.add(file, line_no, 1, "S03", "warning",
                     "'and then' joins two actions: split the item "
                     "(STRUCTURE rule)")
        first = re.match(r"[A-Za-z'-]+", text)
        if first:
            fw = first.group(0).lower()
            if fw.endswith("ing") and fw not in ("during",):
                self.add(file, line_no, 1, "V04", "warning",
                         f"step starts with {first.group(0)!r}: use the "
                         "imperative form (STRUCTURE rule)")
            elif fw not in CONDITION_WORDS:
                # imperative-style step: condition must come first
                body = text[len(first.group(0)):]
                m = re.search(r"\b(if|when|before|after|unless|until)\b",
                              body, re.IGNORECASE)
                if m:
                    self.add(file, line_no, 1, "S04", "warning",
                             "put the condition before the command "
                             "(STRUCTURE rule)")
        for s in sentences:
            self._check_sentence_caps(file, line_no, s, instruction=True)

    def _is_imperative(self, sentence):
        m = re.match(r"[A-Za-z'-]+", sentence)
        if not m:
            return False
        fw = m.group(0).lower()
        if fw in ("do", "make", "note", "let"):
            return True
        return fw in self.d.approved_verbs

    def _check_sentence_caps(self, file, line_no, sentence, instruction):
        n = count_words(sentence)
        cap = 20 if instruction else 25
        if n > cap:
            kind = "instruction" if instruction else "descriptive sentence"
            self.add(file, line_no, 1, "S01", "error",
                     f"{kind} has {n} words (max {cap}, SENTENCES rule)")

    # -- voice checks --------------------------------------------------------

    def check_voice(self, file, line_no, text):
        m = self.passive_re.search(text)
        if m:
            tail = text[m.end():m.end() + 12]
            by = bool(re.match(r"\s+by\b", tail, re.IGNORECASE))
            msg = (f"possible passive voice {m.group(0)!r}: use active "
                   "voice (VERBS rule)")
            if not by:
                msg += " (confirm: no 'by' agent found)"
            self.add(file, line_no, m.start() + 1, "V01", "warning", msg)
        m = NOMINAL_RE.search(text)
        if m:
            self.add(file, line_no, m.start() + 1, "V02", "warning",
                     f"{m.group(0)!r}: use a verb for the action "
                     "(VERBS rule)")
        m = STACKED_RE.search(text)
        if m:
            self.add(file, line_no, m.start() + 1, "V03", "warning",
                     f"{m.group(0)!r}: no stacked auxiliaries; write the "
                     "direct action (VERBS rule)")

    # -- driver --------------------------------------------------------------

    def lint_text(self, file, text):
        doc = Doc(text)
        self.check_units(file, doc)
        seen_d02 = set()
        for line_no, cleaned in doc.prose_lines:
            self.check_words(file, line_no, cleaned)
            self.check_voice(file, line_no, cleaned)
        # dedupe info-level lockdown findings per word
        out = []
        for f in self.findings:
            if f["rule"] == "D02":
                key = (f["file"], f["message"].split("'")[1])
                if key in seen_d02:
                    continue
                seen_d02.add(key)
            out.append(f)
        self.findings = out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

SEV_ORDER = {"error": 0, "warning": 1, "info": 2}
COLORS = {"error": "\033[31m", "warning": "\033[33m", "info": "\033[36m"}


def main():
    ap = argparse.ArgumentParser(
        description="Lint text against distilled ASD-STE100 rules.")
    ap.add_argument("files", nargs="*", help=".md/.txt files (or stdin)")
    ap.add_argument("--strict", action="store_true",
                    help="full STE100 dictionary checks + lockdown info")
    ap.add_argument("--ignore", default="", help="comma-separated rule ids")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    ignore = {r.strip() for r in args.ignore.split(",") if r.strip()}
    data = load_dictionary()
    linter = Linter(data, strict=args.strict, ignore=ignore)

    inputs = args.files or ["-"]
    for path in inputs:
        if path == "-":
            linter.lint_text("<stdin>", sys.stdin.read())
        else:
            with open(path, encoding="utf-8") as f:
                linter.lint_text(path, f.read())

    findings = sorted(linter.findings,
                      key=lambda f: (f["file"], f["line"], f["col"],
                                     SEV_ORDER[f["severity"]]))
    if args.format == "json":
        json.dump(findings, sys.stdout, indent=1)
        print()
    else:
        use_color = sys.stdout.isatty() and not os.environ.get("NO_COLOR")
        for f in findings:
            sev = f["severity"]
            label = sev.upper()
            if use_color:
                label = f"{COLORS[sev]}{label}\033[0m"
            print(f"{f['file']}:{f['line']}:{f['col']}: "
                  f"{label} {f['rule']}: {f['message']}")
        counts = {}
        for f in findings:
            counts[f["severity"]] = counts.get(f["severity"], 0) + 1
        if findings:
            print(", ".join(f"{counts.get(s, 0)} {s}s"
                            for s in ("error", "warning", "info")
                            if counts.get(s)))
        else:
            print("no findings")
    sys.exit(1 if any(f["severity"] == "error" for f in findings) else 0)


if __name__ == "__main__":
    main()
