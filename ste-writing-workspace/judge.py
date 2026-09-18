#!/usr/bin/env python3
"""Blind A/B judge: fresh claude -p compares with/without outputs without labels."""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SKILL_DIR = Path("/home/Qtmd/skills/ste-writing")
WORKSPACE = Path("/home/Qtmd/skills/ste-writing-workspace")
ITERATION = sys.argv[1] if len(sys.argv) > 1 else "iteration-1"
CFG_A = sys.argv[2] if len(sys.argv) > 2 else "with_skill"
CFG_B = sys.argv[3] if len(sys.argv) > 3 else "without_skill"

# Fixed coin flips, recorded for unblinding after judging.
FLIPS = {"eval-rewrite-slop-readme": False,   # False: A=without, B=with
         "eval-write-pr-description": True,   # True:  A=with,    B=without
         "eval-strict-error-messages": False}

PROMPT = """You are comparing two candidate outputs for the same writing task.

TASK PROMPT GIVEN TO THE WRITER:
{prompt}

EXPECTED OUTPUT:
{expected}
{inputs}
=== OUTPUT A ===
{a}

=== OUTPUT B ===
{b}

Score each output 1-5 (integer) on:
- clarity: easy to understand on first read
- concision: no wasted words, no unrequested content
- coverage: covers what the task asked, without inventing facts
- plain_style: sounds like a careful human wrote it, not marketing or AI

Then declare a winner (A, B, or tie) and explain in at most 3 sentences.
Reply with ONLY a JSON object:
{{"a": {{"clarity": n, "concision": n, "coverage": n, "plain_style": n}},
  "b": {{"clarity": n, "concision": n, "coverage": n, "plain_style": n}},
  "winner": "A"|"B"|"tie", "reason": "..."}}"""

def judge(ev):
    name = ev["name"]
    eval_dir = WORKSPACE / ITERATION / name
    a_cfg_text = "\n".join(p.read_text()
                           for p in (eval_dir / CFG_A / "outputs").rglob("*.md"))
    b_cfg_text = "\n".join(p.read_text()
                           for p in (eval_dir / CFG_B / "outputs").rglob("*.md"))
    a_text, b_text = ((a_cfg_text, b_cfg_text) if FLIPS[name]
                      else (b_cfg_text, a_cfg_text))
    inputs = ""
    for f in ev["files"]:
        p = SKILL_DIR / f
        inputs += f"\nINPUT FILE {p.name} GIVEN TO THE WRITER:\n{p.read_text()}\n"
    prompt = PROMPT.format(prompt=ev["prompt"], expected=ev["expected_output"],
                           inputs=inputs, a=a_text, b=b_text)
    proc = subprocess.run(["claude", "-p", prompt, "--output-format", "json",
                           "--dangerously-skip-permissions"],
                          capture_output=True, text=True, timeout=600, cwd="/tmp")
    data = json.loads(proc.stdout)
    result = data.get("result", "")
    start = result.find("{")
    scores = json.loads(result[start:]) if start >= 0 else {"raw": result}
    record = {"blind_scores": scores,
              "mapping": {"A": CFG_A if FLIPS[name] else CFG_B,
                          "B": CFG_B if FLIPS[name] else CFG_A}}
    (eval_dir / "judge.json").write_text(json.dumps(record, indent=2))
    return name, scores.get("winner"), record["mapping"]

def main():
    evals = json.loads((SKILL_DIR / "evals" / "evals.json").read_text())["evals"]
    with ThreadPoolExecutor(max_workers=3) as pool:
        for name, winner, mapping in pool.map(judge, evals):
            print(f"{name}: blind winner={winner} mapping={mapping}", flush=True)

if __name__ == "__main__":
    main()
