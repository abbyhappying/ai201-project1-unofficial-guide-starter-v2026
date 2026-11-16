"""Score each criteria.md target per run from results/final_runs/runN/.
Prints a per-run detail block and writes results/final_runs/summary.json."""
import json
import re
import statistics as st
import sys
from pathlib import Path

REPO = Path.cwd()
OUT = REPO / "results" / "final_runs"
sys.path.insert(0, str(REPO))
import gate  # noqa: E402
from questions import OUT_OF_SCOPE  # noqa: E402

RIGHT_DOC = {"A_laundry": r"housing_\w+_laundry", "B_drop": r"admin_add_drop_deadline",
             "C_printing": r"admin_printing_quota"}


def recs(d, name):
    p = d / f"{name}.records.jsonl"
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def cites(record, pattern):
    ans = (record.get("output") or {}).get("answer") or ""
    return bool(re.search(pattern, ans))


def score(n):
    d = OUT / f"run{n}"
    res = {}

    # C1: laundry chain, memory on, turns 2 and 3
    a = recs(d, "c1c2_A_laundry_memory_on")
    rows = []
    for r in a[1:3]:
        q, s = r["input"]["question"], r["input"]["standalone_question"]
        ok = s != q and re.search(r"laundry|dryer", s, re.I) and not re.search(r"\bit\b", s, re.I)
        rows.append((q, s, bool(ok)))
    res["c1"] = {"pass": sum(x[2] for x in rows), "of": 2, "rows": rows}

    # C2A: turn 2 of each chain, memory off vs on
    a_rows = []
    for key, pat in RIGHT_DOC.items():
        on = recs(d, f"c1c2_{key}_memory_on")[1]
        off = recs(d, f"c2_{key}_memory_off")[1]
        off_bad = off["status"] == "refused" or not cites(off, pat)
        on_good = on["status"] == "ok" and cites(on, pat)
        a_rows.append((key, off["status"], cites(off, pat), on["status"], cites(on, pat), off_bad and on_good))
    # C2B: off-topic turn 4 of each memory-on chain
    b_rows = []
    for key in RIGHT_DOC:
        r = recs(d, f"c1c2_{key}_memory_on")[3]
        s = r["input"]["standalone_question"]
        b_rows.append((key, s, s == r["input"]["question"], r["status"], cites(r, r"gym")))
    res["c2"] = {"A": a_rows, "A_pass": sum(x[-1] for x in a_rows),
                 "B": b_rows, "B_unchanged": sum(x[2] for x in b_rows),
                 "B_gym_doc": sum(x[4] for x in b_rows)}

    # C3: warm-up + 5 out-of-scope in one session
    c = recs(d, "c3_out_of_scope")
    warm = [r for r in c if r["status"] == "ok"]
    median_ok = st.median(r["duration_ms"]["total"] for r in warm) if warm else None
    rows = []
    for q in OUT_OF_SCOPE:
        mine = [r for r in c if r["input"]["question"] == q]
        r = mine[0] if mine else {}
        ok = (len(mine) == 1 and r.get("status") == "refused"
              and r["output"]["answer"] == gate.REFUSAL
              and r["usage"]["model_calls"] in (0, 1)
              and median_ok is not None and r["duration_ms"]["total"] < median_ok)
        rows.append((q, len(mine), r.get("status"), r.get("usage", {}).get("model_calls"),
                     r.get("duration_ms", {}).get("total"), bool(ok)))
    res["c3"] = {"pass": sum(x[-1] for x in rows), "of": 5, "median_answered_ms": median_ok,
                 "answered_runs": len(warm), "rows": rows}

    # C4: ten single runs, memory off
    t = [recs(d, f"c4_cost_{i:02d}")[0] for i in range(1, 11)]
    tot = [r["usage"]["tokens"]["total"] for r in t]
    cost_ok = all(
        abs(r["usage"]["est_cost_usd"] - round(
            r["usage"]["tokens"]["prompt"] * r["settings"]["price_input_per_m"] / 1e6
            + r["usage"]["tokens"]["output"] * r["settings"]["price_output_per_m"] / 1e6, 6)) < 1e-9
        for r in t)
    spread = (max(tot) - min(tot)) / st.mean(tot)
    res["c4"] = {
        "nonzero": sum(x > 0 for x in tot), "cost_formula_ok": cost_ok,
        "tokens_mean": round(st.mean(tot), 1), "tokens_min": min(tot), "tokens_max": max(tot),
        "spread_pct": round(spread * 100, 2),
        "prompt_mean": round(st.mean(r["usage"]["tokens"]["prompt"] for r in t), 1),
        "output_mean": round(st.mean(r["usage"]["tokens"]["output"] for r in t), 1),
        "ms_mean": round(st.mean(r["duration_ms"]["total"] for r in t), 1),
        "memory": {r["settings"]["memory"] for r in t} == {False},
        "pass": all(x > 0 for x in tot) and cost_ok and spread < 0.10,
    }

    # C5: variant index + log + chunk headers
    v = recs(d, "c5_ask_v2")
    variant_ok = bool(v) and v[0]["settings"]["variant"] == "v2"
    pb = []
    for name in ("c5_chunks_laundry", "c5_chunks_drop"):
        text = (d / f"{name}.txt").read_text(encoding="utf-8")
        pb += re.findall(r"produced by: (\S+)", text)
    pb_ok = bool(pb) and all(p in ("chunker.py::split_documents", "chunker.py::fallback_split") for p in pb)
    idx = (d / "c5_index_v2.txt").read_text(encoding="utf-8")
    res["c5"] = {"variant_logged": v[0]["settings"]["variant"] if v else None,
                 "produced_by": sorted(set(pb)), "chunks_seen": len(pb),
                 "index_exit0": "# exit code: 0" in idx, "pass": variant_ok and pb_ok}
    return res


if __name__ == "__main__":
    runs = [int(x) for x in sys.argv[1:]] or [1, 2, 3]
    summary = {n: score(n) for n in runs}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=list),
                                      encoding="utf-8")
    for n, r in summary.items():
        print(f"\n===== RUN {n}")
        for k, v in r.items():
            print(k, json.dumps(v, ensure_ascii=False, default=list))
