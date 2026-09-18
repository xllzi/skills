#!/usr/bin/env python3
"""Run ste_lint.py on every output file of an iteration; save lint.json per run dir."""
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

SKILL_DIR = Path("/home/Qtmd/skills/ste-writing")
WORKSPACE = Path("/home/Qtmd/skills/ste-writing-workspace")
ITERATION = sys.argv[1] if len(sys.argv) > 1 else "iteration-1"
STRICT_EVALS = {"eval-strict-error-messages"}

def lint_file(path, strict):
    cmd = ["python3", str(SKILL_DIR / "scripts" / "ste_lint.py"), "--format", "json"]
    if strict:
        cmd.append("--strict")
    cmd.append(str(path))
    proc = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return [{"parse_error": proc.stdout[:300], "stderr": proc.stderr[:300]}]

def main():
    root = WORKSPACE / ITERATION
    for eval_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        strict = eval_dir.name in STRICT_EVALS
        for cfg_dir in sorted(p for p in eval_dir.iterdir() if p.is_dir()):
            config = cfg_dir.name
            run_dir = eval_dir / config
            out_dir = run_dir / "outputs"
            if not out_dir.is_dir():
                continue
            report = {"strict": strict, "files": {}, "totals": Counter()}
            for f in sorted(out_dir.rglob("*.md")):
                findings = lint_file(f, strict)
                counts = Counter(x.get("rule", "PARSE_ERROR") for x in findings)
                sev = Counter(x.get("severity", "?") for x in findings)
                report["files"][f.name] = {"findings": findings, "by_rule": dict(counts),
                                           "by_severity": dict(sev)}
                report["totals"].update(counts)
            report["totals"] = dict(report["totals"])
            (run_dir / "lint.json").write_text(json.dumps(report, indent=2))
            print(f"{eval_dir.name}/{config}: {report['totals'] or 'clean'}")

if __name__ == "__main__":
    main()
