"""
Structured run log: one JSON object per line in config.LOG_PATH
(logs/requests.jsonl by default).

Every question asked, from the command line or over HTTP, writes exactly one
record, including runs that crash. Append-only JSONL rather than one JSON
array, so each record is a single write, a crash can't corrupt earlier
records, and the file can be read back line by line:

    python app.py logs              the last 10 records, summarised
    python app.py logs -n 50        the last 50
    python app.py logs --raw        the records as stored, one JSON per line

Fields, per record:

    schema          record format version, bumped if fields change meaning
    ts              UTC timestamp, ISO 8601
    run_id          unique per record
    session_id      one per process: groups the turns of one chat session
    turn            1, 2, 3... within the session
    source          "cli" or "http"
    status          "ok", "refused" or "error"
    input           question (as typed), standalone_question (what was
                    searched), rewritten, history_turns
    output          answer, sources (or error type and message)
    duration_ms     total, plus per stage: rewrite, retrieve, generate
    retrieval       best_distance, threshold, every chunk retrieved with its
                    distance
    usage           model calls, cache hits and tokens for THIS record only,
                    tokens split by stage (rewrite vs generate), and
                    est_cost_usd from the PRICE_*_PER_M settings in config.py
    settings        the knobs that produced this answer: corpus, variant,
                    model, embedding model, top_k, hybrid, memory, cache

Hosts wipe the disk on restart, so serve.py also echoes each line to stdout,
where the host's log viewer keeps it.
"""

import json
import sys
import uuid
from datetime import datetime, timezone

import config

SCHEMA = 1
SESSION_ID = uuid.uuid4().hex[:12]
_turn = 0


def _settings(corpus: str, variant: str) -> dict:
    return {
        "corpus": corpus,
        "variant": variant,
        "model": config.MODEL,
        "embedding_model": config.EMBEDDING_MODEL,
        "top_k": config.TOP_K,
        "hybrid": config.HYBRID,
        "memory": config.MEMORY,
        "cache": config.CACHE_ENABLED,
        "price_input_per_m": config.PRICE_INPUT_PER_M,
        "price_output_per_m": config.PRICE_OUTPUT_PER_M,
    }


def _base(source: str) -> dict:
    global _turn
    _turn += 1
    return {
        "schema": SCHEMA,
        "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "run_id": uuid.uuid4().hex[:12],
        "session_id": SESSION_ID,
        "turn": _turn,
        "source": source,
    }


def _append(record: dict, echo: bool) -> dict:
    """Write one record. Never raises: logging must not break answering."""
    line = json.dumps(record, ensure_ascii=False)
    try:
        config.LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(config.LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError as exc:
        print(f"  [log] could not write {config.LOG_PATH}: {exc}", file=sys.stderr)
    if echo:
        print(line, flush=True)
    return record


def write(
    outcome: dict,
    source: str,
    corpus: str,
    variant: str = "default",
    echo: bool = False,
) -> dict:
    """Log one completed ask_pipeline outcome (answered or refused)."""
    record = _base(source)
    record.update(
        {
            "status": "refused" if outcome.get("refused") else "ok",
            "input": {
                "question": outcome.get("question"),
                "standalone_question": outcome.get("standalone_question"),
                "rewritten": outcome.get("rewritten", False),
                "history_turns": outcome.get("history_turns", 0),
            },
            "output": {
                "answer": outcome.get("answer"),
                "sources": outcome.get("sources", []),
            },
            "duration_ms": {
                "total": outcome.get("latency_ms"),
                **outcome.get("stage_ms", {}),
            },
            "retrieval": {
                "best_distance": round(float(outcome.get("best_distance", 0.0)), 4),
                "threshold": outcome.get("threshold"),
                "results": outcome.get("retrieved", []),
            },
            "usage": {
                "model_calls": outcome.get("model_calls"),
                "cache_hits": outcome.get("cache_hits"),
                "tokens": outcome.get("tokens"),
                # rewrite = what memory costs; generate = the answer itself
                "tokens_by_stage": outcome.get("tokens_by_stage", {}),
                "est_cost_usd": outcome.get("est_cost_usd"),
            },
            "settings": _settings(corpus, variant),
        }
    )
    return _append(record, echo)


def write_error(
    question: str,
    exc: BaseException,
    source: str,
    corpus: str,
    variant: str = "default",
    history_turns: int = 0,
    latency_ms: int | None = None,
    echo: bool = False,
) -> dict:
    """Log a run that raised before producing an outcome."""
    record = _base(source)
    record.update(
        {
            "status": "error",
            "input": {"question": question, "history_turns": history_turns},
            "output": {
                "error_type": type(exc).__name__,
                "error": str(exc)[:1000],
            },
            "duration_ms": {"total": latency_ms},
            "settings": _settings(corpus, variant),
        }
    )
    return _append(record, echo)


def read(n: int | None = None) -> list[dict]:
    """The last n records (all if n is None). Skips lines that aren't valid
    JSON, e.g. one cut short by a crash mid-write."""
    if not config.LOG_PATH.exists():
        return []
    records = []
    with open(config.LOG_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records[-n:] if n else records


def summarise(record: dict) -> str:
    """One readable block per record, for `python app.py logs`.

    Tolerates the older flat records written before schema 1."""
    if "schema" not in record:
        return (
            f"{record.get('ts', '?')}  [legacy]  {record.get('question')!r}  "
            f"refused={record.get('refused')}  {record.get('latency_ms')}ms"
        )

    inp = record.get("input", {})
    out = record.get("output", {})
    dur = record.get("duration_ms", {})
    status = record.get("status", "?")
    head = (
        f"{record['ts']}  {status.upper():7}  "
        f"session {record.get('session_id')} turn {record.get('turn')}  "
        f"{dur.get('total')}ms"
    )
    lines = [head, f"  Q: {inp.get('question')}"]
    if inp.get("rewritten"):
        lines.append(f"  searched as: {inp.get('standalone_question')}")
    if status == "error":
        lines.append(f"  error: {out.get('error_type')}: {out.get('error')}")
    else:
        ret = record.get("retrieval", {})
        usage = record.get("usage", {})
        tokens = (usage.get("tokens") or {}).get("total")
        by_stage = usage.get("tokens_by_stage") or {}
        split = ", ".join(
            f"{stage} {t.get('total')}" for stage, t in by_stage.items() if t.get("total")
        )
        stages = ", ".join(
            f"{k} {v}" for k, v in dur.items() if k != "total"
        )
        lines.append(f"  A: {(out.get('answer') or '').strip()[:200]}")
        lines.append(
            f"  best distance {ret.get('best_distance')} (cutoff "
            f"{ret.get('threshold')})"
        )
        lines.append(
            f"  cost: {usage.get('model_calls')} model calls, {tokens} tokens"
            f"{f' ({split})' if split else ''}, ${usage.get('est_cost_usd', 0):.6f}"
            f"{f'  | ms: {stages}' if stages else ''}"
        )
    return "\n".join(lines)
