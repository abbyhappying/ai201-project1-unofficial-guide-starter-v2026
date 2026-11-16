"""Run every criteria.md check once per run (3 runs), saving raw CLI output
and the exact log records each step produced, under results/final_runs/runN/.

Usage (from the repo root):  .venv/Scripts/python.exe <this file> 1 2 3
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path.cwd()
PY = str(REPO / ".venv" / "Scripts" / "python.exe")
LOG = REPO / "logs" / "requests.jsonl"
OUT = REPO / "results" / "final_runs"

CHAINS = {
    "A_laundry": ["Where can I do laundry?", "How much does it cost?", "What about the dryer?"],
    "B_drop": ["What's the class drop deadline?", "What about adding one?", "Does it show on my transcript?"],
    "C_printing": ["How does the printing quota work?", "How much does it cost?", "What happens if I run out?"],
}
OFF_TOPIC = "Where is the gym?"
WARMUP = "Where can I do laundry?"

sys.path.insert(0, str(REPO))
from questions import OUT_OF_SCOPE  # noqa: E402


def log_lines():
    return LOG.read_text(encoding="utf-8").splitlines() if LOG.exists() else []


def run(step_dir, name, args, stdin=None, memory="1"):
    env = dict(os.environ, AI201_CACHE="0", AI201_MEMORY=memory,
               AI201_CORPUS="campus_life", PYTHONIOENCODING="utf-8")
    before = len(log_lines())
    p = subprocess.run([PY, "app.py", "--corpus", "campus_life", *args],
                       input=stdin, capture_output=True, text=True,
                       encoding="utf-8", env=env, cwd=REPO)
    records = [json.loads(l) for l in log_lines()[before:] if l.strip()]
    cmd = f"AI201_CACHE=0 AI201_MEMORY={memory} python app.py --corpus campus_life {' '.join(args)}"
    (step_dir / f"{name}.txt").write_text(
        f"$ {cmd}\n" + (f"# stdin:\n{stdin}\n" if stdin else "") +
        f"# exit code: {p.returncode}\n\n{p.stdout}\n{p.stderr}", encoding="utf-8")
    (step_dir / f"{name}.records.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")
    calls = sum((r.get("usage") or {}).get("model_calls") or 0 for r in records)
    print(f"  {name}: exit {p.returncode}, {len(records)} log records, {calls} model calls", flush=True)
    # Free tier: 15 requests/minute per project, and the app's limiter only
    # counts calls inside one process. Pace across processes at ~10/minute.
    time.sleep(max(2, 6 * calls))
    return p, records


def one_run(n):
    d = OUT / f"run{n}"
    d.mkdir(parents=True, exist_ok=True)
    print(f"Run {n}", flush=True)
    for key, turns in CHAINS.items():
        run(d, f"c1c2_{key}_memory_on", ["ask"], "\n".join(turns + [OFF_TOPIC]) + "\n\n", "1")
        run(d, f"c2_{key}_memory_off", ["ask"], "\n".join(turns) + "\n\n", "0")
    run(d, "c3_out_of_scope", ["ask"], "\n".join([WARMUP, *OUT_OF_SCOPE]) + "\n\n", "1")
    for i in range(1, 11):
        run(d, f"c4_cost_{i:02d}", ["ask", WARMUP], None, "0")
    run(d, "c5_index_v2", ["--variant", "v2", "index"])
    run(d, "c5_ask_v2", ["--variant", "v2", "ask", WARMUP], None, "0")
    run(d, "c5_chunks_laundry", ["chunks", "--from-doc", "housing_aldridge_hall_laundry"])
    run(d, "c5_chunks_drop", ["chunks", "--from-doc", "admin_add_drop_deadline"])


if __name__ == "__main__":
    time.sleep(65)  # let the earlier burst's minute window clear
    for n in sys.argv[1:]:
        one_run(int(n))
