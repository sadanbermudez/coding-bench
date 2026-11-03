"""coding-bench: can a local or free model replace Claude Code?

Each task in tasks/<id>/ has task.md (the instruction), repo/ (the starting code) and
grade/test_hidden.py (tests the agent never sees). For every (agent, task) pair the
runner copies repo/ into a fresh work folder, runs the agent there with the task as
its prompt, then copies in the hidden test and runs it. A task passes only if every
hidden test passes.

  python run.py --verify                      # prove tasks are fair (start fails, reference passes)
  python run.py --agents qwen --only 01,02    # quick try
  python run.py --agents claude,qwen,deepseek # full run, then results/<stamp>.md

Agents run the real tools (Claude Code, OpenCode), so the result measures the whole
harness + model, which is what "replace Claude Code" means.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
TASKS = HERE / "tasks"
SOLUTIONS = HERE / "solutions"
RESULTS = HERE / "results"
WORK = Path(os.environ.get("TEMP", "/tmp")) / "coding-bench-runs"
OPENCODE = Path(r"C:\Users\sadan\tools\opencode\node_modules\opencode-windows-x64\bin\opencode.exe")
OPENCODE_CONFIG = Path(r"C:\Users\sadan\my-agent\argus\coder\opencode.json")
CLAUDE = shutil.which("claude") or str(Path.home() / ".local/bin/claude.exe")

SUFFIX = ("\n\nWork in the current directory. Use only the Python standard library. "
          "When the task is done, stop.")

AGENTS = {
    # Claude Code on the subscription. acceptEdits + allowed tools so it never waits for a prompt.
    "claude": {"kind": "claude", "model": "claude-opus-5-5", "label": "Claude Code + Opus 5.5"},
    "sonnet": {"kind": "claude", "model": "claude-sonnet-5-5", "label": "Claude Code + Sonnet 5.5"},
    "qwen": {"kind": "opencode", "model": "jarvis-local/Qwen3.6-35B-A3B-UD-Q4_K_M",
             "label": "OpenCode + Qwen3.6-35B (local)"},
    "deepseek": {"kind": "opencode", "model": "opencode/deepseek-v4.1-flash-free",
                 "label": "OpenCode + DeepSeek V4.1 Flash (free, Zen)"},
    # DeepSeek's own harness on the same local Qwen: isolates harness vs model (compare with "qwen").
    # Model + approval settings live in tools/dsh/home/profiles/headless/cordis.patch.yml.
    "dsh-qwen": {"kind": "dsh", "label": "DeepSeek Harness + Qwen3.6-35B (local)"},
}
DSH_BIN = Path(r"C:\Users\sadan\tools\dsh\node_modules\@deepseek-ai\dsh\lib\bin.js")
DSH_HOME = Path(r"C:\Users\sadan\tools\dsh\home")
LLAMA_KEY_FILE = Path(os.path.expandvars(r"%LOCALAPPDATA%\hermes\runtimes\llamacpp\.api_key"))


def copy_repo(task: Path, dest: Path) -> None:
    if dest.exists():
        def unlock(fn, path, _exc):  # git object files are read-only on Windows
            os.chmod(path, 0o666)
            fn(path)
        shutil.rmtree(dest, onerror=unlock)
    shutil.copytree(task / "repo", dest)
    subprocess.run(["git", "-c", "core.autocrlf=false", "init", "-q"], cwd=dest, check=True)
    subprocess.run(["git", "-c", "core.autocrlf=false", "add", "-A"], cwd=dest, check=True)
    subprocess.run(["git", "-c", "core.autocrlf=false", "-c", "user.name=bench", "-c", "user.email=bench@local", "commit", "-qm", "start"],
                   cwd=dest, check=True)


def grade(task: Path, work: Path) -> dict:
    """Run the hidden tests in `work`. Returns passed/total counts."""
    test = work / "_hidden_test.py"
    shutil.copy(task / "grade" / "test_hidden.py", test)
    try:
        r = subprocess.run([sys.executable, "-I", str(test)], cwd=work, capture_output=True, text=True,
                           timeout=600, encoding="utf-8", errors="replace")
        out = r.stderr + r.stdout
        code = r.returncode
    except subprocess.TimeoutExpired:
        out, code = "hidden tests timed out", -1
    finally:
        test.unlink(missing_ok=True)
    m = re.search(r"Ran (\d+) test", out)
    total = int(m.group(1)) if m else 0
    bad = sum(int(x) for x in re.findall(r"(?:failures|errors)=(\d+)", out))
    passed = max(total - bad, 0) if total else 0
    return {"pass": code == 0 and total > 0, "tests_passed": passed, "tests_total": total,
            "grade_tail": out[-1500:] if code else ""}


def run_agent(agent: dict, prompt: str, work: Path, timeout: int) -> dict:
    env = dict(os.environ)
    if agent["kind"] == "claude":
        cmd = [CLAUDE, "-p", "--model", agent["model"], "--output-format", "json",
               "--permission-mode", "acceptEdits", "--allowedTools", "Bash,Read,Edit,Write,Glob,Grep",
               "--max-turns", "60"]
        stdin = prompt
    elif agent["kind"] == "dsh":
        env["DSH_HOME"] = str(DSH_HOME)
        env["JARVIS_LLAMA_KEY"] = LLAMA_KEY_FILE.read_text(encoding="utf-8").strip()
        cmd = ["node", str(DSH_BIN), "--profile", "headless", "--json", "-"]   # task text on stdin
        stdin = prompt
    else:
        env["OPENCODE_CONFIG"] = str(OPENCODE_CONFIG)
        cmd = [str(OPENCODE), "run", "-m", agent["model"], "--format", "json", "--dir", str(work), prompt]
        stdin = None
    t0 = time.perf_counter()
    try:
        r = subprocess.run(cmd, cwd=work, input=stdin, capture_output=True, text=True, timeout=timeout,
                           env=env, encoding="utf-8", errors="replace")
        out, err, code, timed_out = r.stdout, r.stderr, r.returncode, False
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        err, code, timed_out = "", None, True
    secs = time.perf_counter() - t0
    (work.parent / f"{work.name}.agent.log").write_text(out + "\n--- stderr ---\n" + err, encoding="utf-8")
    info = {"seconds": round(secs, 1), "exit": code, "timed_out": timed_out}
    info.update(usage(agent, out))
    return info


def usage(agent: dict, out: str) -> dict:
    """Best-effort token / cost numbers from the agent's JSON output."""
    if agent["kind"] == "claude":
        try:
            j = json.loads(out.strip().splitlines()[-1])
            u = j.get("usage", {})
            return {"turns": j.get("num_turns"), "cost_usd": j.get("total_cost_usd"),
                    "out_tokens": u.get("output_tokens"),
                    "in_tokens": (u.get("input_tokens") or 0) + (u.get("cache_read_input_tokens") or 0)
                    + (u.get("cache_creation_input_tokens") or 0)}
        except (ValueError, IndexError):
            return {}
    tin = tout = steps = 0
    for line in out.splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        part = ev.get("part") or {}
        tok = part.get("tokens") if isinstance(part, dict) else None
        if ev.get("type") == "step_finish" and tok:
            steps += 1
            tin += (tok.get("input") or 0) + ((tok.get("cache") or {}).get("read") or 0)
            tout += (tok.get("output") or 0) + (tok.get("reasoning") or 0)
    return {"turns": steps or None, "in_tokens": tin or None, "out_tokens": tout or None}


def power() -> str:
    """'AC' or 'battery NN%' (timings of local models depend on it)."""
    try:
        # Win32_Battery.BatteryStatus flips to 1 while charging on this laptop; PowerOnline is reliable.
        r = subprocess.run(["powershell", "-NoProfile", "-Command",
                            "$w=Get-CimInstance -Namespace root/wmi -ClassName BatteryStatus | Select -First 1; "
                            "$b=Get-CimInstance Win32_Battery; \"$($w.PowerOnline) $($b.EstimatedChargeRemaining)\""],
                           capture_output=True, text=True, timeout=30)
        online, pct = r.stdout.split()
        return "AC" if online == "True" else f"battery {pct}%"
    except Exception:
        return "unknown"


def pick(only: str | None) -> list[Path]:
    tasks = sorted(p for p in TASKS.iterdir() if (p / "task.md").exists())
    if only:
        keys = [k.strip() for k in only.split(",") if k.strip()]
        tasks = [t for t in tasks if any(t.name.startswith(k) or t.name == k for k in keys)]
    return tasks


def verify(tasks: list[Path]) -> int:
    bad = 0
    for t in tasks:
        w = WORK / "verify" / t.name
        copy_repo(t, w)
        start = grade(t, w)
        for f in (SOLUTIONS / t.name).rglob("*"):
            if f.is_file():
                dst = w / f.relative_to(SOLUTIONS / t.name)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(f, dst)
        ref = grade(t, w)
        ok = (not start["pass"]) and ref["pass"]
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {t.name:22} start {start['tests_passed']}/{start['tests_total']}"
              f"  reference {ref['tests_passed']}/{ref['tests_total']}")
        if not ref["pass"]:
            print(ref["grade_tail"])
    return 1 if bad else 0


def report(rows: list[dict], names: list[str], stamp: str) -> str:
    lines = [f"# coding-bench run {stamp}", "", "| Agent | Tasks passed | Hidden tests passed | Median time | Total time |",
             "|---|---|---|---|---|"]
    for n in names:
        mine = [r for r in rows if r["agent"] == n]
        if not mine:
            continue
        secs = sorted(r["seconds"] for r in mine)
        med = secs[len(secs) // 2]
        lines.append(f"| {AGENTS[n]['label']} | {sum(r['pass'] for r in mine)}/{len(mine)} | "
                     f"{sum(r['tests_passed'] for r in mine)}/{sum(r['tests_total'] for r in mine)} | "
                     f"{med:.0f} s | {sum(secs) / 60:.1f} min |")
    for n in names:
        states = sorted({r.get("power", "unknown") for r in rows if r["agent"] == n})
        if states:
            lines.append(f"\n{AGENTS[n]['label']}: power during run: {', '.join(states)}")
    lines += ["", "## Per task", "", "| Task | " + " | ".join(AGENTS[n]["label"] for n in names) + " |",
              "|---|" + "---|" * len(names)]
    for t in sorted({r["task"] for r in rows}):
        cells = []
        for n in names:
            r = next((x for x in rows if x["agent"] == n and x["task"] == t), None)
            cells.append("-" if not r else f"{'PASS' if r['pass'] else 'fail'} {r['tests_passed']}/{r['tests_total']}"
                         f" ({r['seconds']:.0f} s{', timeout' if r['timed_out'] else ''})")
        lines.append(f"| {t} | " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agents", default="qwen")
    ap.add_argument("--only")
    ap.add_argument("--timeout", type=int, default=900, help="seconds per agent per task")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    tasks = pick(a.only)
    if a.verify:
        return verify(tasks)
    names = [n.strip() for n in a.agents.split(",") if n.strip()]
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    RESULTS.mkdir(exist_ok=True)
    jsonl = RESULTS / f"{stamp}.jsonl"
    rows = []
    for n in names:
        for t in tasks:
            w = WORK / stamp / n / t.name
            w.parent.mkdir(parents=True, exist_ok=True)
            copy_repo(t, w)
            prompt = (t / "task.md").read_text(encoding="utf-8") + SUFFIX
            info = run_agent(AGENTS[n], prompt, w, a.timeout)
            g = grade(t, w)
            row = {"agent": n, "task": t.name, "power": power(), **info, **g}
            rows.append(row)
            with jsonl.open("a", encoding="utf-8") as f:
                f.write(json.dumps(row) + "\n")
            print(f"{n:9} {t.name:22} {'PASS' if g['pass'] else 'fail'} {g['tests_passed']}/{g['tests_total']}"
                  f"  {info['seconds']:6.0f} s{'  TIMEOUT' if info['timed_out'] else ''}", flush=True)
    md = report(rows, names, stamp)
    (RESULTS / f"{stamp}.md").write_text(md, encoding="utf-8")
    print("\n" + md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
