# Acceptance criteria

Five numbered criteria for the Milestone 3/4 hand-in. Three are about the
extension (conversation memory), one about the cost measurement, one about the
bad path. Each target is a number, a rate, or something a person can plainly
see. Under each, why that target and not a stricter or looser one.

---

## 1. Memory rewrites both follow-ups in a 3-turn chain into standalone questions that name the subject

**Target:** For a 3-turn chain (`Where can I do laundry?` → `How much does it
cost?` → `What about the dryer?`), **both** follow-ups (turns 2 and 3) produce a
`standalone_question` that (a) differs from the typed question and (b) names the
subject the previous turn was about (contains "laundry" or "dryer", not "it").
Checked by reading the `(searched as: ...)` lines and `logs/requests.jsonl`.

**Why this target, not stricter or looser:** A 3-turn chain has exactly 2
follow-ups, so "both" is the only honest count — "2 of 3" would be counting a
turn that cannot rewrite by design (turn 1 has no history). A looser target
("at least 1 of 2") would pass even if the rewriter fired once by luck. Being
wrong here costs the whole point of memory: a follow-up that still says "it"
retrieves the same noisy chunks as no memory at all.

---

## 2. Memory turns a scattered or refused follow-up into a focused, correctly-sourced answer

**Target:** Run the same 3-turn chain twice, once with `AI201_MEMORY=0` and
once with `=1`. Look at the **second turn** (the first follow-up). Without
memory it is **either refused (`best_distance > 0.6`) or covers ≥2 topics**
(a topic is one of: laundry, printing, transcripts, drop deadline, housing
non-laundry, or anything else). With memory it is **answered
(`best_distance < 0.6`), covers exactly 1 topic, and every cited source is a
housing document (`housing_*`)**. Checked on 3 chains: laundry, drop
deadline, printing quota.

**Why this target, not stricter or looser:** Stricter ("all 3 chains must
improve") fails on the printing chain, where the corpus has no answer — that
is a corpus limit, not a memory failure. Looser ("at least one chain") could
pass by luck. Three chains and a topic count make the improvement measured,
not asserted. Counting topics is checkable from the `A:` line; "better" is not.


## 3. A refused question is refused cheaply and logged exactly once

**Target:** For 5 out-of-scope questions (`OUT_OF_SCOPE` in the eval set), run
**inside one interactive session after a first warm-up question**, each run
returns `I don't have enough information about that.`, the `duration_ms.total`
is **under the median answered run in the same session**, and
`logs/requests.jsonl` gains **exactly one** record per question with
`"status": "refused"`, `"model_calls": 0` (no history) or `1` (with history, the
rewrite only), and `"output.answer"` equal to the refusal string.

**Why this target, not stricter or looser:** This is the bad-path criterion.
The gate exists so a question the corpus cannot answer never reaches the
generator — that is what makes a refusal cheap and honest. A fixed 400 ms
target fails on cold start: each `python app.py ask` is a new process, and
retrieval alone took 1013–3843 ms in the ten logged runs, mostly loading the
embedding model. Measuring inside one warm session removes that noise. "Under
the median answered run" is the real claim: a refusal skips generation, so it
should be faster than a normal answer, but not instant (retrieval still runs).
A looser target ("under 5 s") would pass even if the generator was being
called, which is the regression this checks for. "Exactly one record" matters
because a refusal that is not logged cannot be audited, and a doubled record
means the ask path wrote twice.

---

## 4. The cost of one run is measured from the service's token counts and reproducible from the log

**Target:** Ten back-to-back runs of `Where can I do laundry?` with
`AI201_CACHE=0` (memory off, noted below) produce 10 records where
`usage.tokens.total` is **non-zero on every run**, `usage.est_cost_usd` equals
`tokens.prompt × settings.price_input_per_m / 1e6 +
tokens.output × settings.price_output_per_m / 1e6`, and the token spread
(max − min) is **under 10% of the mean**. A second person, given only
`logs/requests.jsonl` and `criteria.md`, can recompute the averages and get the
same numbers to 1 decimal place.

**Why this target, not stricter or looser:** `tokens.total` non-zero is the
check that caching is actually off — a run that reports 0 tokens is a cache hit,
and averaging cache hits understates the true cost. `est_cost_usd` non-zero is
**impossible on the free tier**, where the prices are 0, so the criterion
requires the arithmetic to hold instead (0 × 0 = 0 passes). The token spread
target (10%) replaces a latency spread target: the ten runs had max − min =
4742 ms against a mean of 5270 ms (90%), which is network variance, not a
system property; tokens varied by only 1. A looser token bound (50%) would pass
even if the model was padding answers. "Reproducible from the log" is the real
target: `est_cost_usd` is an estimate from `config.PRICE_*_PER_M`, so the record
must carry the unit price it used (it does, in `settings`). Being wrong here
costs the whole measurement: a cost you cannot recompute is a guess with a
decimal point.

**Note on memory:** these runs use `AI201_MEMORY=0`. For a single question
memory makes no difference (no history, no rewrite), so the choice does not
change the numbers; it is stated so the record matches the setting.

---

## 5. Re-chunking and re-indexing stay consistent, and the index can be audited per source

**Target:** After `python app.py index --variant v2`, `python app.py logs`
records from `variant=v2` show `settings.variant == "v2"`, and a chunk printed
by `python app.py chunks --from-doc <name> --variant v2` has a `produced_by`
that names the function actually used for that document (`split_documents` or
`fallback_split`, whichever ran). A person can see this: the `produced_by`
string in the chunk header is one of those two names, and `settings.variant` in
the log matches the variant the chunk came from.

**Why this target, not stricter or looser:** This replaces the earlier
"produced_by identical within a run" target, which could fail legitimately when
one document goes through `fallback_split` and another through
`split_documents` — that is correct behaviour, not a bug. The real failure mode
is re-chunking without re-indexing: the index then answers from chunks that no
longer exist, and `settings.variant` in the log is the only place that would
show it. A stricter target ("every chunk has the same produced_by") would
misclassify the mixed case as a failure. A looser target ("chunks print") would
pass even if the variant in the log did not match the variant searched.
