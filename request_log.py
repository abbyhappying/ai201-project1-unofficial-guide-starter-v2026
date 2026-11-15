"""
Structured request log: one JSON object per line in config.LOG_PATH.

Append-only JSONL rather than one JSON array, so each request is a single
write, a crash can't corrupt earlier entries, and `tail -f` just works.

Hosts wipe the disk on restart, so serve.py also echoes each line to stdout,
where the host's log viewer keeps it.
"""

import json
import sys
from datetime import datetime, timezone

import config


def write(outcome: dict, source: str, corpus: str, echo: bool = False) -> dict:
    """Log one ask_pipeline outcome. Never raises: logging must not break answering."""
    record = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": source,
        "corpus": corpus,
        "question": outcome.get("question"),
        "standalone_question": outcome.get("standalone_question"),
        "history_turns": outcome.get("history_turns", 0),
        "refused": outcome.get("refused"),
        "best_distance": round(float(outcome.get("best_distance", 0.0)), 4),
        "threshold": outcome.get("threshold"),
        "sources": outcome.get("sources", []),
        "latency_ms": outcome.get("latency_ms"),
    }
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
