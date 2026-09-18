#!/usr/bin/env python3
"""Run ste-writing evals with headless claude code, with_skill vs without_skill."""
import json
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SKILL_DIR = Path("/home/Qtmd/skills/ste-writing")
WORKSPACE = Path("/home/Qtmd/skills/ste-writing-workspace")
SNAPSHOT_DIR = WORKSPACE / "skill-snapshot"
ITERATION = sys.argv[1] if len(sys.argv) > 1 else "iteration-1"
# config name -> skill path (None = no skill baseline)
ALL_CONFIGS = {"with_skill": SKILL_DIR, "old_skill": SNAPSHOT_DIR,
               "without_skill": None}
CONFIGS = sys.argv[2:] or ["with_skill", "without_skill"]
MAX_WORKERS = 3
RUN_TIMEOUT_S = 900

def build_prompt(ev, config):
    skill = ALL_CONFIGS[config]
    lines = ["Execute this task:"]
    if skill:
        lines.append(f"- Skill path: {skill}")
    lines.append(f"- Task: {ev['prompt']}")
    files = ", ".join(Path(f).name for f in ev["files"]) or "none"
    lines.append(f"- Input files: {files}")
    lines.append("- Save outputs to: outputs/")
    if skill:
        lines.append("Read the SKILL.md at the skill path first and follow it.")
    return "\n".join(lines)

def run_one(ev, config):
    name = ev["name"]
    run_dir = WORKSPACE / ITERATION / name / config
    out_dir = run_dir / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    for f in ev["files"]:
        shutil.copy(SKILL_DIR / f, run_dir / Path(f).name)

    cmd = ["claude", "-p", build_prompt(ev, config), "--output-format", "json",
           "--dangerously-skip-permissions"]
    if ALL_CONFIGS[config]:
        cmd += ["--add-dir", str(ALL_CONFIGS[config])]

    t0 = time.monotonic()
    proc = subprocess.run(cmd, cwd=run_dir, capture_output=True, text=True,
                          timeout=RUN_TIMEOUT_S)
    wall_ms = int((time.monotonic() - t0) * 1000)

    (run_dir / "stdout.json").write_text(proc.stdout)
    if proc.stderr:
        (run_dir / "stderr.txt").write_text(proc.stderr)

    timing = {"returncode": proc.returncode, "wall_ms": wall_ms}
    try:
        data = json.loads(proc.stdout)
        usage = data.get("usage", {})
        timing.update({
            "total_tokens": sum(usage.get(k, 0) for k in (
                "input_tokens", "output_tokens",
                "cache_read_input_tokens", "cache_creation_input_tokens")),
            "duration_ms": data.get("duration_ms"),
            "num_turns": data.get("num_turns"),
            "total_cost_usd": data.get("total_cost_usd"),
            "model": list(data.get("modelUsage", {}).keys()),
        })
        (run_dir / "result.md").write_text(data.get("result", ""))
    except json.JSONDecodeError:
        timing["parse_error"] = proc.stdout[:500]
    (run_dir / "timing.json").write_text(json.dumps(timing, indent=2))
    return name, config, timing

def main():
    evals = json.loads((SKILL_DIR / "evals" / "evals.json").read_text())["evals"]
    jobs = [(ev, c) for ev in evals for c in CONFIGS]
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        for name, config, timing in pool.map(lambda a: run_one(*a), jobs):
            print(f"{name}/{config}: rc={timing['returncode']} "
                  f"tokens={timing.get('total_tokens')} ms={timing.get('duration_ms')}",
                  flush=True)

if __name__ == "__main__":
    main()
