#!/usr/bin/env python3
"""Extract the ASD-STE100 dictionary (part 2) into ste_dictionary.json.

Usage:
    python3 extract_dictionary.py /path/to/ASD-STE100_ISSUE9.pdf [out.json]

Requires pdftotext (poppler). The source PDF is not distributed with this
skill; the extracted ste_dictionary.json is what ste_lint.py uses at run
time. Layout notes: UPPERCASE headwords are approved words, lowercase
headwords are not approved (their column 2 gives approved alternatives).
"""
import json
import re
import subprocess
import sys
import tempfile



POS = r"(?:n|v|adj|adv|prep|conj|pron|art|num)"
ENTRY_RE = re.compile(rf"^([A-Za-z][A-Za-z'’\- ]*?) *\(({POS})\)(.*)$")
WORD_ONLY_RE = re.compile(r"^[A-Za-z][A-Za-z'’\- ]+$")
POS_ONLY_RE = re.compile(rf"^\(({POS})\)$")
PAGE_RE = re.compile(r"^Page 2-")
NOISE = (
    "Issue 9", "2025-01-15", "Part 2 - Dictionary",
    "ASD-STE100 Simplified Technical English",
    "ASD STE100 Simplified Technical English",
)
MARKER_RE = re.compile(r"\((?:n|v|adj|adv|prep|conj|pron|art|num|TN|TV)\)\.?$")
CAPS_RE = re.compile(r"^[A-Z0-9][A-Z0-9 ,''’/&+.()\-]*\.?$")


def is_caps(text):
    text = MARKER_RE.sub("", text).strip()
    return bool(CAPS_RE.match(text)) and any(c.isalpha() for c in text)


def is_noise(stripped):
    return (not stripped or PAGE_RE.match(stripped)
            or any(stripped.startswith(n) for n in NOISE)
            or stripped in ("Word", "(part of speech)", "ALTERNATIVES",
                            "STE EXAMPLE", "Non-STE example", "Blank Page"))


def main():
    pdf = sys.argv[1] if len(sys.argv) > 1 else None
    if not pdf:
        sys.exit(__doc__)
    out_path = (sys.argv[2] if len(sys.argv) > 2
                else "ste_dictionary.json")
    with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8") as tmp:
        subprocess.run(["pdftotext", "-layout", pdf, tmp.name], check=True)
        lines = open(tmp.name, encoding="utf-8").read().splitlines()

    # Start after the intro (page 2-0-16 footer), at the first table header.
    start = None
    seen_20 = False
    for i, ln in enumerate(lines):
        if re.match(r"^Page 2-0-16", ln.strip()):
            seen_20 = True
        if seen_20 and "Approved meaning/" in ln:
            start = i
            break
    if start is None:
        sys.exit("dictionary start not found")

    approved = {}
    not_approved = {}

    cur = None
    cur_kind = None
    c2 = c3 = 19, 49
    in_restricted = False

    def new_entry(word, pos, rest, col2):
        nonlocal cur, cur_kind, in_restricted
        in_restricted = False
        word = " ".join(word.split())
        if word[0].islower():
            cur_kind = "not"
            cur = not_approved.setdefault(
                word, {"pos": [], "alternatives": []})
            if pos not in cur["pos"]:
                cur["pos"].append(pos)
        else:
            cur_kind = "ok"
            cur = approved.setdefault(
                word, {"pos": [], "meanings": [], "forms": [], "restricted": []})
            if pos not in cur["pos"]:
                cur["pos"].append(pos)
            if rest:
                cur["forms"].extend(
                    f.strip(" .,") for f in rest.split(",")
                    if f.strip(" .,") and is_caps(f.strip(" .,")))
        if col2:
            add_col2(col2)

    def add_col2(text):
        nonlocal in_restricted
        low = text.rstrip(".").lower()
        if low.startswith("for other"):
            in_restricted = True
            return
        if cur_kind == "not":
            if is_caps(text):
                cur["alternatives"].append(text.rstrip("."))
            else:
                cur.setdefault("notes", []).append(text)
        else:
            if in_restricted and is_caps(text):
                cur["restricted"].append(text.rstrip("."))
            else:
                cur["meanings"].append(text)

    def peek_pos_only(idx):
        """Next meaningful line's col1 is a bare '(pos)'?"""
        j = idx + 1
        while j < len(lines):
            s = lines[j].strip()
            if is_noise(s) or "Approved meaning/" in lines[j]:
                j += 1
                continue
            m = POS_ONLY_RE.match(lines[j][:c2].strip())
            return m.group(1) if m else None
        return None

    i = start
    while i < len(lines):
        ln = lines[i].rstrip()
        stripped = ln.strip()

        if "Approved meaning/" in ln:
            c2 = ln.index("Approved")
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if "STE EXAMPLE" in nxt:
                c3 = nxt.index("STE EXAMPLE")
                i += 2
                continue
            i += 1
            continue
        if is_noise(stripped):
            i += 1
            continue

        col1 = ln[:c2].strip()
        col2 = ln[c2:c3].strip() if len(ln) > c2 else ""
        i += 1

        m = ENTRY_RE.match(col1)
        if m:  # Pattern A: "word (pos)" on one line
            new_entry(m.group(1).strip(), m.group(2), m.group(3).strip(), col2)
            continue
        if WORD_ONLY_RE.match(col1):  # Pattern B: pos wrapped to next line
            pos = peek_pos_only(i - 1)
            if pos:
                new_entry(col1, pos, "", col2)
                continue
        if cur is None:
            continue
        if POS_ONLY_RE.match(col1):
            col1 = ""  # wrapped pos of a Pattern B headword: treat as empty
        if col1:
            if cur_kind == "ok":
                chunk = col1.replace("(also", "").replace(")", "")
                for f in chunk.split(","):
                    f = f.strip(" .,")
                    if f and is_caps(f):
                        cur["forms"].append(f)
            continue
        if col2:
            add_col2(col2)

    for ent in approved.values():
        ent["meanings"] = [" ".join(ent["meanings"])] if ent["meanings"] else []
        ent["forms"] = sorted(set(ent["forms"]))

    ANY_MARKER_RE = re.compile(r"\((?:n|v|adj|adv|prep|conj|pron|art|num|TN|TV)\)")
    vocab = set(approved)
    for ent in approved.values():
        vocab.update(ent["forms"])

    def clean(alts):
        # Join consecutive bare fragments when the previous one is a single
        # word: pdf layout can split one alternative ("INCORRECTLY ADJUSTED")
        # across rows.
        joined = []
        for a in alts:
            if joined and " " not in joined[-1] \
                    and not ANY_MARKER_RE.search(joined[-1]) \
                    and not ANY_MARKER_RE.search(a):
                joined[-1] += " " + a
            else:
                joined.append(a)
        # Keep bare (unmarked) alternatives only when every word is approved
        # vocabulary ("GO INTO", "MORE THAN"); drop example-text bleed.
        out = []
        for a in joined:
            a = re.split(r" {2,}", a)[0].strip()  # cut example-column bleed
            if not a:
                continue
            if not ANY_MARKER_RE.search(a):
                words = re.findall(r"[A-Za-z'’]+", a)
                if not words or any(w.upper() not in vocab for w in words):
                    continue
            out.append(a)
        return out

    for ent in not_approved.values():
        ent["alternatives"] = clean(ent["alternatives"])
    for ent in approved.values():
        ent["restricted"] = clean(ent["restricted"])

    out = {"approved": approved, "not_approved": not_approved}
    json.dump(out, open(out_path, "w"), indent=1, ensure_ascii=False, sort_keys=True)
    print(f"wrote {out_path}")
    print(f"approved: {len(approved)}  not-approved: {len(not_approved)}")


if __name__ == "__main__":
    main()
