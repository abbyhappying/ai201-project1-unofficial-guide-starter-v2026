"""Score criterion 2 with the REVISED target, for any result set.

Turn 2 of each chain:
  memory off: refused (best_distance > 0.6) OR covers >= 2 topics
  memory on : answered (best_distance < 0.6), exactly 1 topic, and every cited
              source matches the chain's topic:
              laundry -> housing_*laundry*, drop -> admin_*drop*,
              printing -> admin_*printing*
Topics are read from the files the answer cites.

Usage: python score_c2_revised.py final_runs final_runs_after
"""
import json
import re
import sys
from fnmatch import fnmatch
from pathlib import Path

REPO = Path.cwd()
CHAINS = {"A_laundry": "housing_*laundry*", "B_drop": "admin_*drop*",
          "C_printing": "admin_*printing*"}


def topic(f):
    if fnmatch(f, "housing_*laundry*"):
        return "laundry"
    if f.startswith("housing_"):
        return "housing non-laundry"
    if "printing" in f:
        return "printing"
    if "transcript" in f:
        return "transcripts"
    if "drop" in f:
        return "drop deadline"
    return "other:" + f


def turn2(path):
    r = json.loads(path.read_text(encoding="utf-8").splitlines()[1])
    cited = sorted(set(re.findall(r"[a-z0-9_]+\.txt", r["output"]["answer"] or "")))
    return r, cited


def score(set_name, n):
    d = REPO / "results" / set_name / f"run{n}"
    rows = []
    for key, pat in CHAINS.items():
        off, off_cited = turn2(d / f"c2_{key}_memory_off.records.jsonl")
        on, on_cited = turn2(d / f"c1c2_{key}_memory_on.records.jsonl")
        off_topics = {topic(f) for f in off_cited}
        on_topics = {topic(f) for f in on_cited}
        off_ok = off["status"] == "refused" or len(off_topics) >= 2
        on_ok = (on["status"] == "ok" and on["retrieval"]["best_distance"] < 0.6
                 and len(on_topics) == 1 and bool(on_cited)
                 and all(fnmatch(f, pat) for f in on_cited))
        rows.append({
            "chain": key, "pass": off_ok and on_ok,
            "off": {"status": off["status"], "dist": off["retrieval"]["best_distance"],
                    "topics": sorted(off_topics), "ok": off_ok},
            "on": {"status": on["status"], "dist": on["retrieval"]["best_distance"],
                   "cited": on_cited, "ok": on_ok,
                   "bad_sources": [f for f in on_cited if not fnmatch(f, pat)]},
        })
    return rows


if __name__ == "__main__":
    out = {}
    for s in sys.argv[1:]:
        out[s] = {n: score(s, n) for n in (1, 2, 3)}
        for n, rows in out[s].items():
            print(f"{s} run{n}: {sum(r['pass'] for r in rows)}/3")
            for r in rows:
                print("   ", json.dumps(r, ensure_ascii=False))
    (REPO / "results" / "c2_revised_scores.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
