#!/usr/bin/env python3
"""
The Unofficial Guide — the same pipeline, over HTTP.

    python serve.py                          run it locally on port 5000
    gunicorn serve:app                       run it the way a host runs it

Nothing new happens in this file. It is a wrapper: a request comes in, it
hands the question to `app.py::ask_pipeline` — the exact function the command
line uses — and hands the answer back as JSON. Retrieval, the relevance gate
and the grounded prompt all still live where they lived. If you change how
your system answers, you change it in those files and this one follows.

Two routes:

    POST /ask       {"question": "...", "history": [...]} in, the answer and its sources out
    GET  /health    is the service up, and is there an index to search

`history` is optional: earlier turns as [{"question": ..., "answer": ...}],
oldest first. The client keeps it and sends it back; the server is stateless.

Why this exists: `app.py` runs once and exits, which is fine on your laptop
and impossible to deploy. A hosted service has to stay up and wait for
requests. This is the smallest thing that does that.

Each request is logged by request_log.py to logs/requests.jsonl and echoed to
stdout, because a host's disk doesn't survive a restart but its log viewer does.
"""

import os

from flask import Flask, jsonify, request

import config

app = Flask(__name__)


@app.get("/health")
def health():
    """Is the service up, and is there an index to search?

    Two different questions, and the second one is the one that bites. A
    freshly deployed service answers this route happily while every /ask
    returns "no index" — hosts give you no disk that survives a restart, so
    the index has to be built as part of getting the service up. Checking
    here means you find that out in one request instead of five.
    """
    from store import index_exists

    ready = index_exists(config.CORPUS)
    return jsonify(
        {
            "status": "ok",
            "corpus": config.CORPUS,
            "index_ready": ready,
            "detail": (
                "ready"
                if ready
                else "no index for this corpus — run `python app.py index`"
            ),
        }
    )


@app.post("/ask")
def ask():
    """One question in, one grounded answer out.

    A refused question is a 200, not an error. The gate refusing is your
    system working — it is an answer, and the JSON says so with
    `"refused": true` so whatever calls this can tell the two apart.
    """
    from app import ask_pipeline

    payload = request.get_json(silent=True) or {}
    question = (payload.get("question") or "").strip()

    if not question:
        return (
            jsonify(
                {
                    "error": "Send JSON with a question in it, like "
                    '{"question": "is the housing lottery random?"}'
                }
            ),
            400,
        )

    # Optional conversation memory. The server keeps no state: the client sends
    # the earlier turns back each time, as [{"question": ..., "answer": ...}],
    # oldest first. That survives restarts and works across gunicorn workers.
    history = payload.get("history") or []
    if not isinstance(history, list):
        return (
            jsonify(
                {
                    "error": 'history must be a list like '
                    '[{"question": "...", "answer": "..."}]'
                }
            ),
            400,
        )

    import time

    import request_log

    started = time.perf_counter()
    try:
        outcome = ask_pipeline(question, corpus=config.CORPUS, history=history)
    except Exception as exc:  # noqa: BLE001 — a reader gets this, not a traceback
        request_log.write_error(
            question, exc, source="http", corpus=config.CORPUS,
            history_turns=len(history),
            latency_ms=round((time.perf_counter() - started) * 1000),
            echo=True,
        )
        return jsonify({"error": f"{type(exc).__name__}: {exc}"}), 500

    request_log.write(outcome, source="http", corpus=config.CORPUS, echo=True)

    return jsonify(
        {
            "question": question,
            "standalone_question": outcome["standalone_question"],
            "answer": outcome["answer"],
            "refused": outcome["refused"],
            "sources": outcome["sources"],
            "best_distance": round(outcome["best_distance"], 4),
            "threshold": outcome["threshold"],
            "corpus": config.CORPUS,
        }
    )


def main():
    # Hosts tell you which port to listen on through PORT, and they expect you
    # on 0.0.0.0. Binding 127.0.0.1 instead works perfectly on your laptop and
    # then answers nothing at all once deployed, because the host's router
    # can't reach a socket that only accepts connections from inside the
    # container. It is the single most common way a first deploy "succeeds"
    # and is unreachable.
    port = int(os.getenv("PORT", "5000"))

    # Debug mode reloads on save, which is handy, and prints a console that
    # runs arbitrary code, which is not something to leave switched on where
    # strangers can reach it. Off unless you ask for it.
    debug = os.getenv("AI201_DEBUG", "0") == "1"

    print(f"Serving The Unofficial Guide on http://localhost:{port}")
    print(f"Corpus: {config.CORPUS}    (Ctrl-C to stop)\n")
    print("Try it from another terminal:\n")
    print(f"  curl http://localhost:{port}/health")
    print(
        f"  curl -X POST http://localhost:{port}/ask \\\n"
        f"    -H 'Content-Type: application/json' \\\n"
        f"    -d '{{\"question\": \"is the housing lottery random?\"}}'\n"
    )

    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()
