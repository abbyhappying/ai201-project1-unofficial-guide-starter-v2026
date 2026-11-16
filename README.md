# The Unofficial Guide

I picked the corpus of city_guides and ask "where shall I visit".

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.**  A typed table gets
> full credit; a picture of the same table gets none.
>


---

# Unit 1

## What This Does



python app.py --corpus advice_threads chunks -n 2 Output:
 26 chunks total. Showing 2, spread across the corpus.

======================================================================
Chunk 1  |  source: thread_bike_commute.txt#0  |  produced by: chunker.py::fallback_split
======================================================================
THREAD: Is a bike worth it for a 20 minute walk commute?

--- reply 1 (14 votes) ---
Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.

--- reply 2 (9 votes) ---
Counterpoint, I sold mine. Between November and March the paths are either icy or salted and salt destroysa drivetrain in one season.

--- reply 3 (22 votes) ---
Both true. I keep a cheap bike for September to November and walk the rest of the year. Total cost was about $120 for the bike and I don't care what happens to it.

--- reply 4 (5 votes) ---
If you do get one, the campus does free registration and it's the only reason I got mine back after it wastaken.

======================================================================
Chunk 2  |  source: thread_meal_plan_tier.txt#0  |  produced by: chunker.py::fallback_split
======================================================================
THREAD: Which meal plan tier is right?

--- reply 1 (24 votes) ---
Depends entirely on whether your building has a kitchen. Fenwick has kitchenettes, so people there go downa tier and cook two or three nights. Everywhere else, get the middle tier.

--- reply 2 (19 votes) ---
The highest tier only makes sense if you eat three meals a day in the halls every single day, which basically nobody does past October.

--- reply 3 (11 votes) ---
Remember you can only change it once and only in the first ten days. I waited and got stuck on a plan I didn't use.

--- reply 4 (7 votes) ---
Declining balance rolls within the semester but not between them. Spend it in December or lose it.



## Chunking Strategy

**Chunk size:**

I split on the document's natural structure rather than fixed character counts. For city_guides, that means splitting on ## headings and prepending the # title to each chunk, because all 14 guides share near-identical section names and without the town name the embeddings are indistinguishable. For campus_life, I split on paragraph breaks and merge small paragraphs up to ~450 characters, prepending the title — producing ~110–120 chunks rather than the baseline's 88. CHUNK_SIZE acts as a backstop, not a tuning parameter.

**Overlap:**
0 for both corpora. Because chunks end at structural boundaries (headings for city_guides, paragraph breaks for campus_life), there is no severed context to repair.

## Sample Chunks


**Chunk 1** — source: `` — produced by: ``

======================================================================
Chunk 1  |  source: guide_accessibility.md#0  |  produced by: chunker.py::split_documents
======================================================================
Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are difficult and it is betterto know in advance.


**Chunk 2** — source: `` — produced by: ``

======================================================================
Chunk 2  |  source: guide_corry_vale.md#5  |  produced by: chunker.py::split_documents
======================================================================
Corry Vale — Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.

**Chunk 3** — source: `` — produced by: ``

======================================================================
Chunk 3  |  source: guide_givens_mill.md#2  |  produced by: chunker.py::split_documents
======================================================================
Givens Mill — Getting around

Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.

**Chunk 4** — source: `` — produced by: ``

======================================================================
Chunk 4  |  source: guide_kestrelford.md#4  |  produced by: chunker.py::split_documents
======================================================================
Kestrelford — What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. Theparish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.


**Chunk 5** — source: `` — produced by: ``

======================================================================
Chunk 5  |  source: guide_pellew_sands.md#6  |  produced by: chunker.py::split_documents
======================================================================
Pellew Sands — When to go

June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.

## Sample Answer

<!--  Milestone 4. -->

**Question:**
"where to find local specific food"

**Answer:**
```
(best distance 0.565, cutoff 0.6)

Based on the provided documents, local specific food can be found in the following places:
- Halden Bay, where the two harbour restaurants buy seafood directly from early-morning boats.
- Givens Mill's tearoom, which sells bread made from flour ground twenty metres away.
- Kestrelford's bakery, which sells out by 11am and brings people back.
- Thornby Wells, where Sunday lunch is a local institution requiring a week's advance booking. ```
```
**Question:**
"how to get around this area"

**Answer:**
```
 (best distance 0.535, cutoff 0.6)
Based on the provided documents, getting around depends on the specific location:

* **Thornby Wells:** It is flat, compact, and everything is within three minutes of everything else. Parking is free for two hours anywhere in town, the station is central, and the pump room and gardens are level throughout (*guide_accessibility.md*).
* **Marchwood:** There is a modern tram network with level boarding on all four lines that runs every 8minutes on weekdays, and the city museum and covered market are step-free (*guide_accessibility.md*).
* **Brightwater:** The area is level along the river and through the centre, and the mill museum is step-free. The station is a 15-minute walk from campus on flat ground, or you can take the shuttle which meets the four busiest arrivals (*guide_accessibility.md*).
* **Halden Bay:** The town is small enough to cross in fifteen minutes, though it is built on three levels connected by stepped lanes, and the harbour front is level (*guide_halden_bay.md*).
* **Kestrelford:** Everything is within a ten-minute walk of the market square, though the town is on aslope and there is no local bus service within the town (*guide_kestrelford.md*).
* **Givens Mill:** Everything is on one single street along the river, with the mill and church eight minutes apart at opposite ends, and a riverside path that continues in both directions (*guide_givens_mill.md*).

Sources retrieved: guide_accessibility.md, guide_givens_mill.md, guide_halden_bay.md, guide_kestrelford.md
```

**Question:**
"how was winter here"

**Answer:**
```
(best distance 0.588, cutoff 0.6)

In winter, the path past the pond in Brightwater ices over, and the Kestrelford approach road is impassable in snow, which can cut the town off for a day or two most winters (guide_walking.md and guide_kestrelford.md). Additionally, winter in Halden Bay is described as dramatic and largely closed (guide_halden_bay.md).

Sources retrieved: guide_halden_bay.md, guide_kestrelford.md, guide_seasons.md, guide_thornby_wells.md,guide_walking.md
```

**Question:**
 "how to go to Halden Bay"

**Answer:**
```
  (best distance 0.280, cutoff 0.6)

To get to Halden Bay, you must take the coast road, which is slow (taking 40 minutes for 22 miles) withthe last stretch cut into the cliff. Alternatively, buses run four times a day.

Source: `guide_halden_bay.md` (also mentioned in `guide_regional_transport.md`)

Sources retrieved: guide_halden_bay.md, guide_regional_transport.md, guide_seasons.md
```

**Question:**
"how was Elder Ness"

**Answer:**
```
  (best distance 0.241, cutoff 0.6)

Based on the provided documents, Elder Ness is a headland featuring a village of 300 people, a lighthouse, a bird observatory, and very few other attractions. It is known for being quiet and is visited for birds, walking, or its lack of things to do.

Source: `guide_elder_ness.md`

Sources retrieved: guide_elder_ness.md
```

**Question:**
"how was the transportation in this city"

**Answer:**
```
  (best distance 0.635, cutoff 0.6)

I don't have enough information about that.
```

**Question:**
"where shall I visit"

**Answer:**
```
  (best distance 0.657, cutoff 0.6)

I don't have enough information about that.
```

**Question:**
"what is most popular restaurant"


**Answer:**
```
  (best distance 0.604, cutoff 0.6)

I don't have enough information about that.
```

**Question:**
"how was the safety in downtown"


**Answer:**
```
  (best distance 0.662, cutoff 0.6)

I don't have enough information about that.
```

**Question:**
"where do you recommend to shopping"


**Answer:**
```
  (best distance 0.617, cutoff 0.6)

I don't have enough information about that.
```
**My relevance cutoff:**
```
Cutoff placed at: 0.60

In-scope question distances: 0.565, 0.535, 0.588, 0.280, 0.241 (range 0.241 – 0.588)

Out-of-scope question distances: 0.635, 0.657, 0.604, 0.662, 0.617 (range 0.604 – 0.662)

Gap: 0.588 – 0.604


 The two groups separate with a gap of 0.016 between the highest in-scope distance (0.588) and the lowest out-of-scope distance (0.604). Placing the cutoff at 0.60 sits inside this gap and correctly classifies all 5 in-scope questions as answerable and all 5 out-of-scope questions as refused. The gap is narrow (0.016 wide),0.60 is the safest choice because it sits closest to the middle of the gap, giving the most margin on both sides.
```
| Question | In corpus? | Best distance |
|---|---|---|
where to find local specific food	 Yes	0.565
how to get around this area	 Yes	0.535
how was winter here	 Yes	0.588
how to go to Halden Bay	 Yes	0.280
how was Elder Ness	 Yes	0.241
how was the transportation in this city	 No	0.635
where shall I visit	 No	0.657
what's recommend food in this city	 No	0.604
how was the safety in downtown	 No	0.662
where do you recommend to shopping	 No	0.617

## How I Used AI

**1.**
I used Claude as a coding and reasoning assistant throughout the project — not as a code generator that I accepted wholesale, but as a tool I interrogated, corrected, and made decisions with. Two moments stand out.

Moment 1 — Chunking strategy for city_guides vs campus_life
What I asked for: I pasted the milestone brief into Claude and asked what chunk size and overlap to use for my corpus. I had assumed there was one "correct" number — something like 500 characters that would work for everything.

What came back: Claude pushed back on the premise. It argued that chunk size should be derived from the document's own structure, not from a fixed character count, and walked through why city_guides (long, headed, 14 near-identical "Getting there" sections) and campus_life (short, unheaded, self-contained posts) needed different treatment. It recommended splitting on ## headings for city_guides and paragraph-merging for campus_life.

What I changed: Claude's first version missed the title-prepending step entirely. When I tested it, fourteen chunks all read "Getting there" — embeddings were nearly indistinguishable, and retrieval for a named town was a coin flip. I caught this by running python app.py chunks -n 5 and reading the output, noticed the missing town name, and added the title prefix myself. I also rejected the suggestion to keep campus_life as one document per chunk because it produced byte-for-byte identical output to the starter's fallback_split — which would have failed the milestone. I pushed back, and we settled on paragraph-merging up to ~450 characters instead.


**2.**
What I asked for: I asked Claude to recommend a distance cutoff for the relevance gate. I expected a single number from a rule of thumb.

What came back: Claude said a cutoff couldn't be chosen in the abstract — it had to be derived from my actual distances. It walked me through running my 5 in-scope and 5 out-of-scope questions, recording the best distance for each, and finding the gap between the two groups. My data came back as in-scope 0.241–0.588 and out-of-scope 0.604–0.662 — a narrow 0.016 gap.

What I changed: Claude initially suggested moving the cutoff to 0.59 to "put it in the middle." I disagreed — 0.59 sits closer to the in-scope boundary, which would be riskier if a borderline question shifted. I argued for 0.60, which sits at the midpoint of the actual gap and matches the starter default already validated by my data.



---

# Unit 2


## Run Log — Before



| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 |5/5 | 5/5| MET|
| 2. Every answer names a source | 5 of 5 | 5/5 |5/5 | 5/5| MET|
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 |5/5 | 5/5| MET|
| 4. Chunks hold together (self-contained, ≥200 chars) | 4 of 5 | 5/5 |5/5 | 5/5| MET|
| 5. Stability across 3 runs (same core chunks + equivalent answers)|| 4 of 5 | 5/5 |5/5 | 5/5| MET|





If I want to eat dinner at 9:30pm, which town in the region can I actually get a hot meal in?
  run 1: pass  (best distance 0.564)
  run 2: pass  (best distance 0.564)
  run 3: pass  (best distance 0.564)

How early do I need to arrive in Halden Bay to find parking on a summer weekend?
  run 1: pass  (best distance 0.293)
  run 2: pass  (best distance 0.293)
  run 3: pass  (best distance 0.293)

Which walking route in the region gives the most for the least effort, and how long is it?
  run 1: pass  (best distance 0.435)
  run 2: pass  (best distance 0.435)
  run 3: pass  (best distance 0.435)

Which town in the region is easiest to get around with limited mobility?
  run 1: pass  (best distance 0.463)
  run 2: pass  (best distance 0.463)
  run 3: pass  (best distance 0.463)

How often does the access road to Elder Ness flood, and for how long each time?
  run 1: pass  (best distance 0.276)
  run 2: pass  (best distance 0.276)
  run 3: pass  (best distance 0.276)

Out-of-scope questions (the gate should refuse these):
  refused  (best distance 0.808)  What is the capital of Mongolia?
  refused  (best distance 0.881)  How do I change the oil in a diesel engine?
  refused  (best distance 0.982)  Who won the 1994 World Cup?
  refused  (best distance 0.835)  What is the recommended dosage of ibuprofen for a headache?
  refused  (best distance 0.859)  How do I write a for loop in Rust?
  -> gate refused 5 of 5

Wrote results\run_2026-09-26_1033_before.md
15 model calls this session, 9849 tokens (9063 in, 786 out)



## Verdicts


| # | Criterion | Verdict | How I decided |
| 1 | 	Retrieved chunks contain the answer (target: 4 of 5) |	MET |	All 5 in-scope questions returned an answer-bearing chunk in all 3 runs; best distances 0.276–0.564, every one under the 0.6 gate. |
| 2 | 	Every answer names a source (target: 5 of 5) |MET |	Citation is a deterministic formatting step — source metadata is attached at index time and carried through retrieval, so all 5 answers cited a source in all 3 runs. |
| 3 | Relevance gate stops out-of-corpus questions (target: 4 of 5) |MET |	All 5 out-of-scope questions were refused in all 3 runs; best distances 0.808–0.982, every one well above the 0.6 cutoff. (Target held; the description under this criterion in criteria.md has stale numbers and needs a revision underneath, not an edit.) |
| 4 | Chunks hold together — self-contained and ≥200 chars (target: 4 of 5) |MET |All sampled chunks in every run started and ended at natural boundaries with no severed sentences, and all cleared the 200-character floor. |
| 5 | Stability across 3 runs — same core chunks + semantically equivalent answers (target: 4 of 5)	 |MET |Every distance was byte-identical across all 3 runs (e.g. 0.564/0.564/0.564) and answers were semantically equivalent, confirming the pipeline is deterministic. |

## Diagnoses

I missed nothing, all 5 criteria met in all 3 runs.


## The Improvement

**What I changed:**
Criterion 3 of gate stops out-of-corpus 4 of 5 tries changed to 5 of 5 tries.

**Why I picked it:**
The target might be too low since the original 4/5 was justified by a claimed thin 0.10 gap with an overlap zone,but the measured data shows a 0.24 clean gap — in-scope tops out at 0.564, out-of-scope bottoms out at 0.808, with the 0.6 cutoff sitting well inside the empty middle. With that separation, there's no borderline case,I should set 5 of 5 out-of-scope questions refused. This is a broken measurement, I'd prefer tighten from 4 of 5 to 5 of 5.



### Run Log — After



| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |

| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 |5/5 | 5/5| MET|
| 2. Every answer names a source | 5 of 5 | 5/5 |5/5 | 5/5| MET|
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 |5/5 | 5/5| MET|
| 4. Chunks hold together (self-contained, ≥200 chars) | 4 of 5 | 5/5 |5/5 | 5/5| MET|
| 5. Stability across 3 runs (same core chunks + equivalent answers)|| 4 of 5 | 5/5 |5/5 | 5/5| MET|

  run 2: pass  (best distance 0.293)
  run 3: pass  (best distance 0.293)

Which walking route in the region gives the most for the least effort, and how long is it?
  run 1: pass  (best distance 0.435)
  run 2: pass  (best distance 0.435)
  run 3: pass  (best distance 0.435)

Which town in the region is easiest to get around with limited mobility?
  run 1: pass  (best distance 0.463)
  run 2: pass  (best distance 0.463)
  run 3: pass  (best distance 0.463)

How often does the access road to Elder Ness flood, and for how long each time?
  run 1: pass  (best distance 0.276)
  run 2: pass  (best distance 0.276)
  run 3: pass  (best distance 0.276)

Out-of-scope questions (the gate should refuse these):
  refused  (best distance 0.808)  What is the capital of Mongolia?
  refused  (best distance 0.881)  How do I change the oil in a diesel engine?
  refused  (best distance 0.982)  Who won the 1994 World Cup?
  refused  (best distance 0.835)  What is the recommended dosage of ibuprofen for a headache?
  refused  (best distance 0.859)  How do I write a for loop in Rust?
  -> gate refused 5 of 5

Wrote results\run_2026-09-27_1303_after.md
15 model calls this session, 10124 tokens (9327 in, 797 out)

**Did it help?**

Hybrid search helped. It moved the answer-bearing chunk from rank 6 to rank 2 on the one question vector search got wrong.
That flipped the answer from wrong to right.
It left the other four questions and the gate's refusal behavior unchanged.

## What's Still Broken
Retrieved chunks contain the answer — target 4 of 5

The retrieval is now genuinely 5/5. The measurement is broken, and it was hiding a real failure.

scorer.py::judge is expects.lower() in answer.lower(). For Q1 my expects is "Marchwood", and the before-run answers were "there is no mention of any town in the region where you can get a hot meal at 9:30pm (kitchens outside Marchwood stop serving at 9pm)". The token appears inside the negation, so it scored pass while saying the opposite of the right answer. My Before table says 5/5; the true before was 4/5.

The criterion has a second problem: it is about retrieved chunks, but scorer.py only ever sees the answer text. Those come apart in both directions — a right answer can be guessed from a neighbouring chunk, a wrong answer can be produced from a correct one. Criterion 1 is not measured by the thing measuring it.

## What I'd Do Differently

I'd rewrite criterion 1 to be measured at the retrieval layer — does the answer-bearing chunk's label appear in top-5, because my old scorer graded the answer text while claiming to grade retrieval, and that's why the hybrid win was invisible.

##  How I use AI
Moment 1 — Spotting the pattern in my Q1 failures
What I asked for:
I pasted the three failing Q1 answers from the run log side by side and asked Claude to look for what they had in common. I'd been reading them one at a time and they each felt like separate mistakes.

What came back:
It flagged that all three said the same thing in different words — "there is no mention of any town…", "I do not have enough information…". A negation pattern. Then it pointed at scorer.py::judge and noted the expected token "Marchwood" appears inside "kitchens outside Marchwood stop serving at 9pm", so the substring match passed a negated answer.

What I changed about it:
I didn't take the diagnosis on faith — I opened scorer.py and confirmed line 4 was expects.lower() in answer.lower(), then grepped the run log for "Marchwood" and saw it only appeared in that negating clause. Two things I corrected myself:

Moment 2 — Stress-testing the RRF design before building it
What I asked for:
I described the hybrid plan in plain terms — build BM25 from Chroma at query time, fuse by rank with RRF, keep distance as-is — and asked Claude what could silently break. I specifically wanted failure modes, not a pep talk.

What came back:
Two traps I hadn't considered:

Putting the fused score into Result.distance. RRF scores are unitless ranks, so a perfect match and "What is the capital of Mongolia?" both score ~0.0164 — the gate would pass everything and my Milestone 4 calibration would be meaningless.

Fusion reorders the truncated list. If the vector-nearest chunk (distance 0.55) got pushed to rank 6 by fusion, the gate would see a best distance of 0.62 and refuse a question it used to answer. Its suggested fix: force the dense top-1 to survive fusion, so min(distance) stays bit-identical.

What I changed about it:
I verified both against the actual code rather than accepting them:

## The Shape

I am taking **Shape C — Extend one capability**. The system I am extending is
the Unofficial Guide RAG pipeline I built in Units 1 and 2. The new capability
is **multi-turn memory**: today the system is stateless, so a follow-up like
"how do I get there in winter?" is embedded on its own, lands far from every
chunk, and is refused by the relevance gate before the model sees it. I am
adding a query-rewrite step that runs only on follow-up turns: the recent
turns are passed to the model, which rewrites the follow-up into a standalone
question (resolving "there" into the named town), and only that rewritten
question is embedded, gated, and answered. The stored documents, the chunker,
the gate cutoff and the generation prompt all stay as they were; what changes is
what gets searched. Memory is off by default via an environment variable
(`AI201_MEMORY=0`) so the same test scripts can be run with and without it and
the two result sets can be compared.

## Out of Scope

Three things I considered and deliberately did not do:

1. **I am not adding cross-session storage.** History lives only for the
   length of one conversation and is held by the caller (the command line loop,
   or the client sending JSON to `/ask`). I am not adding a database, user
   accounts, or a server-side session store. Persisting memory across sessions
   would raise questions about privacy and expiry that are a different unit's
   work.

2. **I am not changing the retrieval strategy.** The hybrid vector + BM25
   search, the chunking, and the 0.6 relevance gate are the system I already
   built and validated. Multi-turn memory sits *in front of* retrieval — it
   changes the question, not how the question is matched. I am not adding a
   second retriever or re-tuning the cutoff, because then a before/after
   comparison could not tell me whether memory helped or whether the new
   retriever did.

3. **I am not rebuilding the interface.** The CLI (`python app.py ask`) and the
   existing `/ask` endpoint stay as they are apart from accepting a history
   list and returning the rewritten question. I am not adding a chat UI, and I
   am not rewriting `serve.py` around a session framework. The point of this
   unit is one bounded capability plus the evidence it works, not a new
   front end.

## Instrumentation

Every question asked through `python app.py ask` (or `POST /ask`) appends one
JSON record to `logs/requests.jsonl`, including runs that crash. The logger is
`request_log.py`; `python app.py logs` reads the file back
(`-n 50`, `--raw`, `--errors`). Each record has named fields:

| Field | What it holds |
|---|---|
| `ts`, `run_id`, `session_id`, `turn` | UTC timestamp, a unique ID per record, one ID per chat session, turn number within it |
| `status` | `ok`, `refused` (relevance gate said no) or `error` |
| `input` | the question as typed, the `standalone_question` actually searched, whether it was `rewritten`, how many `history_turns` were used |
| `output` | the answer and its sources, or `error_type` + `error` |
| `duration_ms` | `total`, plus `rewrite`, `retrieve`, `generate` |
| `retrieval` | `best_distance`, `threshold`, every retrieved chunk with its distance |
| `usage` | `model_calls`, `cache_hits`, `tokens` (prompt / output / total), `tokens_by_stage`, `est_cost_usd` |
| `settings` | corpus, model, embedding model, top_k, hybrid, memory, cache, prices used |

### Ten runs

How I measured: I ran the same question, `Where can I do laundry?`, ten times
against `campus_life`, each as its own `python app.py ask "..."` command, with
the response cache off (`AI201_CACHE=0`) so every run made a real model call.
Times are wall-clock, measured inside `ask_pipeline` with
`time.perf_counter()`. Token counts are what Gemini reported back for the call
(`usage_metadata`), not an estimate.

The entries below are the real records from `logs/requests.jsonl`, shortened
for reading: the answer and error text are cut to their first ~100
characters, and `settings`, `retrieval.results` and `usage.tokens_by_stage` are
left out. Those were the same on every run: gemini-3.5-flash-lite,
all-MiniLM-L6-v2, top_k 5, hybrid on, memory on, cache off, prices 0. One
complete record follows the list.

```jsonl
{"schema": 1, "ts": "2026-11-15T18:17:58.609+00:00", "run_id": "005a1f79eccf", "session_id": "40eedbef5e00", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "Based on the provided documents, you can do laundry in the following locations:  * Aldridg ...", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 5239, "rewrite": 0, "retrieve": 1820, "generate": 3419}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 111, "total": 681}, "est_cost_usd": 0.0}}
{"schema": 1, "ts": "2026-11-15T18:18:04.398+00:00", "run_id": "f4bee5827087", "session_id": "d4e42e089f7f", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "Based on the provided documents, you can do laundry in the following locations: - Aldridge ...", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 3607, "rewrite": 0, "retrieve": 1013, "generate": 2594}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 111, "total": 681}, "est_cost_usd": 0.0}}
{"schema": 1, "ts": "2026-11-15T18:18:10.286+00:00", "run_id": "d3bb31d4ab50", "session_id": "0d290a9dd1fa", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "You can do laundry in the following locations, based on the provided documents: - Aldridge ...", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 3859, "rewrite": 0, "retrieve": 1021, "generate": 2838}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 111, "total": 681}, "est_cost_usd": 0.0}}
{"schema": 1, "ts": "2026-11-15T18:18:20.843+00:00", "run_id": "5d991682514b", "session_id": "f4a9f9792176", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "Based on the provided documents, you can do laundry in the following locations:  * Aldridg ...", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 8349, "rewrite": 0, "retrieve": 3843, "generate": 4502}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 111, "total": 681}, "est_cost_usd": 0.0}}
{"schema": 1, "ts": "2026-11-15T18:18:28.475+00:00", "run_id": "d1d1e027f6eb", "session_id": "00e5f19a4d33", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "Based on the provided documents, you can do laundry in the following locations:  * Aldridg ...", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 4645, "rewrite": 0, "retrieve": 1559, "generate": 3086}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 111, "total": 681}, "est_cost_usd": 0.0}}
{"schema": 1, "ts": "2026-11-15T18:18:36.865+00:00", "run_id": "f434fc8e077c", "session_id": "1a8e24f6b18b", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "Based on the provided documents, you can do laundry in the following locations:  * Aldridg ...", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 5062, "rewrite": 0, "retrieve": 1543, "generate": 3518}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 111, "total": 681}, "est_cost_usd": 0.0}}
{"schema": 1, "ts": "2026-11-15T18:18:46.064+00:00", "run_id": "6a82eefefc51", "session_id": "4e6306cfad13", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "Based on the provided documents, you can do laundry in the following locations:  * Aldridg ...", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 5764, "rewrite": 0, "retrieve": 2098, "generate": 3666}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 111, "total": 681}, "est_cost_usd": 0.0}}
{"schema": 1, "ts": "2026-11-15T18:18:56.710+00:00", "run_id": "9139bdbaf3fe", "session_id": "34e52f164e67", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "Based on the provided documents, you can do laundry in the following locations:  * Aldridg ...", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 6833, "rewrite": 0, "retrieve": 1705, "generate": 5128}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 111, "total": 681}, "est_cost_usd": 0.0}}
{"schema": 1, "ts": "2026-11-15T18:19:04.402+00:00", "run_id": "8c883836040c", "session_id": "0ea7766f5ce7", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "You can do laundry in the following locations, as found in their respective documents: - A ...", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 5339, "rewrite": 0, "retrieve": 1305, "generate": 4033}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 112, "total": 682}, "est_cost_usd": 0.0}}
{"schema": 1, "ts": "2026-11-15T18:19:10.361+00:00", "run_id": "cc0e72c324c9", "session_id": "1fa5532b5aa1", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "You can do laundry in the following locations, as stated in their respective documents: -  ...", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 4004, "rewrite": 0, "retrieve": 1191, "generate": 2813}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 112, "total": 682}, "est_cost_usd": 0.0}}
```

**Failed run.** I tested the failure path by running the same question with an
invalid API key. Retrieval and the gate passed (best distance 0.352), then the
model call was rejected. The run was logged as `status: "error"` with the
exception type and message, and the CLI exited with code 1:

```jsonl
{"schema": 1, "ts": "2026-11-15T18:23:18.218+00:00", "run_id": "4c2455d95269", "session_id": "5c6d98b33048", "turn": 1, "source": "cli", "status": "error", "input": {"question": "Where can I do laundry?", "history_turns": 0}, "output": {"error_type": "ClientError", "error": "400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 's ..."}, "duration_ms": {"total": 4380}}
```

One complete, unshortened record (run 1):

```json
{
  "schema": 1,
  "ts": "2026-11-15T18:17:58.609+00:00",
  "run_id": "005a1f79eccf",
  "session_id": "40eedbef5e00",
  "turn": 1,
  "source": "cli",
  "status": "ok",
  "input": {
    "question": "Where can I do laundry?",
    "standalone_question": "Where can I do laundry?",
    "rewritten": false,
    "history_turns": 0
  },
  "output": {
    "answer": "Based on the provided documents, you can do laundry in the following locations:\n\n* Aldridge Hall (housing_aldridge_hall_laundry.txt)\n* Innisfree Hall (housing_innisfree_hall_laundry.txt)\n* Old Brewhouse (housing_old_brewhouse_laundry.txt)\n* Tamsin Court (housing_tamsin_court_laundry.txt)\n* Fenwick Court (housing_fenwick_court_laundry.txt)",
    "sources": [
      "housing_aldridge_hall_laundry.txt",
      "housing_fenwick_court_laundry.txt",
      "housing_innisfree_hall_laundry.txt",
      "housing_old_brewhouse_laundry.txt",
      "housing_tamsin_court_laundry.txt"
    ]
  },
  "duration_ms": {
    "total": 5239,
    "rewrite": 0,
    "retrieve": 1820,
    "generate": 3419
  },
  "retrieval": {
    "best_distance": 0.3521,
    "threshold": 0.6,
    "results": [
      {
        "source": "housing_aldridge_hall_laundry.txt",
        "distance": 0.4128
      },
      {
        "source": "housing_innisfree_hall_laundry.txt",
        "distance": 0.3977
      },
      {
        "source": "housing_old_brewhouse_laundry.txt",
        "distance": 0.3521
      },
      {
        "source": "housing_tamsin_court_laundry.txt",
        "distance": 0.4502
      },
      {
        "source": "housing_fenwick_court_laundry.txt",
        "distance": 0.4287
      }
    ]
  },
  "usage": {
    "model_calls": 1,
    "cache_hits": 0,
    "tokens": {
      "prompt": 570,
      "output": 111,
      "total": 681
    },
    "tokens_by_stage": {
      "rewrite": {
        "prompt": 0,
        "output": 0,
        "total": 0
      },
      "generate": {
        "prompt": 570,
        "output": 111,
        "total": 681
      }
    },
    "est_cost_usd": 0.0
  },
  "settings": {
    "corpus": "campus_life",
    "variant": "default",
    "model": "gemini-3.5-flash-lite",
    "embedding_model": "all-MiniLM-L6-v2",
    "top_k": 5,
    "hybrid": true,
    "memory": true,
    "cache": false,
    "price_input_per_m": 0.0,
    "price_output_per_m": 0.0
  }
}
```

### Averages over the ten runs

| Measure | Mean | Median | Min | Max | Std dev |
|---|---|---|---|---|---|
| Total time (ms) | 5270 | 5151 | 3607 | 8349 | 1452 |
| Retrieve (ms) | 1710 | 1551 | 1013 | 3843 | 827 |
| Generate (ms) | 3560 | 3469 | 2594 | 5128 | 806 |
| Prompt tokens | 570 | 570 | 570 | 570 | 0 |
| Output tokens | 111.2 | 111 | 111 | 112 | 0.4 |
| Total tokens | 681.2 | 681 | 681 | 682 | 0.4 |
| Model calls | 1 | 1 | 1 | 1 | 0 |
| Best distance | 0.3521 | 0.3521 | 0.3521 | 0.3521 | 0 |

Retrieval and tokens were identical every run; the variation is all time.
Generation (the network call to Gemini) is about two thirds of the total.
Retrieval runs locally, but each run was a fresh process, so its time likely
includes loading the embedding model and index each time. That would explain
why it swings from 1.0 s to 3.8 s. I didn't time that load separately.

## What It Costs

**One run costs 1 model call, about 681 tokens (570 in, 111 out) and about
5.3 seconds. On the free Gemini tier that is $0.00.**

Method: the numbers are the means of the ten logged runs above. Tokens come
from Gemini's own usage report on each response, split per stage in
`usage.tokens_by_stage`. Dollar cost is computed per record as
`prompt_tokens × PRICE_INPUT_PER_M / 1,000,000 + output_tokens × PRICE_OUTPUT_PER_M / 1,000,000`.
Both prices are set in `config.py` (or `.env`) and are 0 because this project
runs on the free tier, so every record logs `est_cost_usd: 0.0`. On a paid key,
putting the model's real prices in `.env` makes the same field report dollars
with no code change.

Since the dollar cost is zero, the real cost is **requests against the free
tier's quota**, and secondly time. That's why `model_calls` is logged on every
record. A first question costs 1 call. With memory on, a follow-up costs **2**:
one to rewrite it into a standalone question and one to answer. In a separate
two-turn test (not one of the ten above), the follow-up used 1036 tokens:
275 for the rewrite and 761 for the answer. So memory roughly doubles the
quota use of every follow-up. An answer served from the response cache costs
0 calls and 0 tokens, and is counted in `usage.cache_hits`.

## Final project-Run Log

Every criterion in `criteria.md` was run three separate times on `campus_life`
with `AI201_CACHE=0`, so every answer is a real model call. The raw CLI output
and the exact log records from each step are saved in
`results/final_runs/run1/`, `run2/` and `run3/`: one `.txt` file (the command,
its input, exit code and full output) and one `.records.jsonl` file per step.
`results/final_runs/summary.json` has the per-run numbers. All 63 steps exited
with code 0.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Follow-ups rewritten to name the subject | both follow-ups (2/2) | 2/2 | 2/2 | 2/2 | **MET** |
| 2. Memory improves answers, doesn't hurt on topic change | A: follow-up fixed by memory on 3 chains; B: off-topic question unchanged **and** cites a gym doc | A 3/3 · B unchanged 3/3, gym doc 0/3 | A 3/3 · B unchanged 3/3, gym doc 0/3 | A 3/3 · B unchanged 3/3, gym doc 0/3 | **PARTLY MET** |
| 3. Refusals cheap and logged once | 5/5 refused, faster than the answered run, 1 record each, ≤1 model call | 5/5 | 5/5 | 5/5 | **MET** |
| 4. Cost measured and reproducible | 10/10 non-zero tokens, cost formula holds, token spread < 10% | 10/10, spread 1.6% | 10/10, spread 2.3% | 10/10, spread 4.3% | **MET** |
| 5. Variant index auditable | log shows `variant: v2`, `produced_by` names a real chunker function | v2, `split_documents` | v2, `split_documents` | v2, `split_documents` | **MET** (narrowly) |

### What each run showed

**1. Rewrite names the subject.** The rewrites were nearly identical in all
three runs:

- Turn 2, `How much does it cost?` → `How much does it cost to do laundry in Aldridge Hall, Innisfree Hall, Old Brewhouse, Tamsin Court, and Fenwick Court?`
- Turn 3, `What about the dryer?` → `How much does it cost to use the dryer in Aldridge Hall, …` (run 1) / `What does it cost to use the dryer in …` (runs 2, 3)

Every rewrite differs from what was typed and names laundry or the dryer.
(My scoring script first marked these 0/2 because it rejected any "it" at all,
including the "does it cost" construction. I checked all six by hand.)
The over-rewriting noted in `criteria.md` is still there: the rewriter copies
the five-building list from the previous answer into every follow-up.

**2A. Memory improves the follow-up.** Turn 2 of each chain, memory off vs. on:

| Chain | Memory off | Memory on |
|---|---|---|
| Laundry: `How much does it cost?` | answered, but untargeted: lists laundry, printing and transcript costs at once (best distance 0.5819, just under the 0.6 cutoff) | laundry prices per building, cites `housing_*_laundry.txt` |
| Drop deadline: `What about adding one?` | **refused** | "through the end of the second week", cites `admin_add_drop_deadline.txt` |
| Printing: `How much does it cost?` | the same untargeted list as the laundry chain (same retrieval, distance 0.5819), or "you have not specified what 'it' refers to" (run 3) | printing cost, cites `admin_printing_quota.txt` |

Without memory, `How much does it cost?` retrieves the same chunks whatever the
conversation was about. That is the failure this criterion targets, in all
three chains and all three runs. (My scoring script first gave runs 1 and 2
2/3, because the untargeted list happens to mention the printing file. Reading
the answers shows it isn't a targeted answer.)

**2B. Topic change.** After each chain, `Where is the gym?` was passed through
unchanged (3/3 every run), so memory did not drag the old topic into a new
question. But it was refused every time, because **campus_life has no gym
document**. The "cites a gym document" half of the target can't be met with
this corpus, which is why the verdict is *partly met*. The target should name
a topic the corpus covers (for example `Where is the health center?`).

**3. Refusals.** In one session, after the warm-up question
`Where can I do laundry?`:

| | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Warm-up (answered) | 2650 ms | 2430 ms | 2500 ms |
| 5 refusals | 500–812 ms | 468–875 ms | 536–1186 ms |
| Records per question | 1 each | 1 each | 1 each |
| `model_calls` per refusal | 1 (the rewrite, since there was history) | 1 | 1 |

Every answer was exactly `I don't have enough information about that.` One
caveat: with only one answered run per session, "the median answered run" is a
single number, and it includes loading the embedding model.

**4. Cost.** Ten runs per pass of `Where can I do laundry?`, memory off:

| | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Mean tokens (prompt / output) | 683.0 (570 / 113.0) | 682.4 (570 / 112.4) | 680.3 (570 / 110.3) |
| Token range | 680–691 | 675–691 | 662–691 |
| Spread (max − min) / mean | 1.6% | 2.3% | 4.3% |
| Mean time | 2663 ms | 3614 ms | 3247 ms |
| `est_cost_usd` = tokens × logged prices | holds on 10/10 ($0, free tier) | 10/10 | 10/10 |

**5. Variant.** `python app.py --variant v2 index` built the index, and an ask
against it logged `settings.variant: "v2"`. The chunk headers for
`housing_aldridge_hall_laundry` and `admin_add_drop_deadline` both name
`chunker.py::split_documents`. This passes, but narrowly: both documents are a
single chunk, and `fallback_split` was never exercised. The command in
`criteria.md` also needs correcting: `--variant` goes **before** the
subcommand (`python app.py --variant v2 index`), and `chunks` re-chunks the
files rather than reading an index, so it has no `--variant` option.

### Failed run

The first attempt at run 1 was aborted. The printing chain hit Gemini's
free-tier limit of **15 requests per minute**
(`429 RESOURCE_EXHAUSTED … GenerateRequestsPerMinutePerProjectPerModel-FreeTier`).
The app's limiter is set to 30 per minute and counts only within one process,
and its retries back off for about 15 s in total, while Google asked for 60 s.
The follow-up was logged as `status: "error"` with the full message. The
output is kept in `results/final_runs/aborted_rate_limited/`. The three runs
above were then re-run from scratch, paced at about 10 calls per minute, and
none of them failed.


### Real output, one run per criterion

Each block below is copied unedited from a real run. The log lines are
whole lines from `logs/requests.jsonl` (line numbers given) from my own
terminal session on 2026-11-16, 04:16–04:28 UTC. Every log line is written by
**`request_log.py::write`**, called from `app.py::_ask_one` right after
`app.py::ask_pipeline` returns. The fields inside each record come from the
functions named under each block. Criterion 5's chunk listing is the saved
terminal output of the scripted run 1 (`results/final_runs/run1/`), because I
didn't save that one from my own terminal.

#### 1. Memory rewrites both follow-ups

Laundry chain with `AI201_MEMORY=1`, session `9bf70bbbf90b`, lines 216–218.
Turn 2's `standalone_question` names laundry; turn 3's names the dryer.

- `input.standalone_question` comes from **`generate.py::rewrite_question`**
  (history trimmed by `generate.py::trim_history`), called in
  `app.py::ask_pipeline`.

```jsonl
{"schema": 1, "ts": "2026-11-16T04:17:37.534+00:00", "run_id": "f4980107bcd6", "session_id": "9bf70bbbf90b", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry", "standalone_question": "Where can I do laundry", "rewritten": false, "history_turns": 0}, "output": {"answer": "You can do laundry at Aldridge Hall (housing_aldridge_hall_laundry.txt), Tamsin Court (housing_tamsin_court_laundry.txt), Innisfree Hall (housing_innisfree_hall_laundry.txt), Old Brewhouse (housing_old_brewhouse_laundry.txt), and Fenwick Court (housing_fenwick_court_laundry.txt).", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 3518, "rewrite": 0, "retrieve": 996, "generate": 2522}, "retrieval": {"best_distance": 0.354, "threshold": 0.6, "results": [{"source": "housing_aldridge_hall_laundry.txt", "distance": 0.4095}, {"source": "housing_tamsin_court_laundry.txt", "distance": 0.4447}, {"source": "housing_innisfree_hall_laundry.txt", "distance": 0.3982}, {"source": "housing_old_brewhouse_laundry.txt", "distance": 0.354}, {"source": "housing_fenwick_court_laundry.txt", "distance": 0.4335}]}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 569, "output": 92, "total": 661}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}, "generate": {"prompt": 569, "output": 92, "total": 661}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": true, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
{"schema": 1, "ts": "2026-11-16T04:17:42.001+00:00", "run_id": "c139dfd9394a", "session_id": "9bf70bbbf90b", "turn": 2, "source": "cli", "status": "ok", "input": {"question": "How much does it cost?", "standalone_question": "How much does it cost to do laundry at Aldridge Hall, Tamsin Court, Innisfree Hall, Old Brewhouse, and Fenwick Court?", "rewritten": true, "history_turns": 1}, "output": {"answer": "Based on the provided documents:\n- **Aldridge Hall:** $1.75 wash, $1.50 dry (housing_aldridge_hall_laundry.txt)\n- **Innisfree Hall:** $1.75 wash, $1.75 dry (housing_innisfree_hall.txt)\n- **Old Brewhouse:** $1.50 wash, $1.50 dry (housing_old_brewhouse.txt and housing_old_brewhouse_laundry.txt)\n- **Fenwick Court:** $2.00 wash, $1.75 dry (housing_fenwick_court_laundry.txt)\n\nThe documents do not contain any information about Tamsin Court, so I do not have enough information to answer for it.", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall.txt", "housing_old_brewhouse.txt", "housing_old_brewhouse_laundry.txt"]}, "duration_ms": {"total": 2696, "rewrite": 1287, "retrieve": 104, "generate": 1304}, "retrieval": {"best_distance": 0.3135, "threshold": 0.6, "results": [{"source": "housing_fenwick_court_laundry.txt", "distance": 0.3135}, {"source": "housing_innisfree_hall.txt", "distance": 0.3389}, {"source": "housing_aldridge_hall_laundry.txt", "distance": 0.3239}, {"source": "housing_old_brewhouse.txt", "distance": 0.3223}, {"source": "housing_old_brewhouse_laundry.txt", "distance": 0.3571}]}, "usage": {"model_calls": 2, "cache_hits": 0, "tokens": {"prompt": 785, "output": 208, "total": 993}, "tokens_by_stage": {"rewrite": {"prompt": 222, "output": 33, "total": 255}, "generate": {"prompt": 563, "output": 175, "total": 738}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": true, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
{"schema": 1, "ts": "2026-11-16T04:17:48.906+00:00", "run_id": "9ae299d2a899", "session_id": "9bf70bbbf90b", "turn": 3, "source": "cli", "status": "ok", "input": {"question": "What about the dryer?", "standalone_question": "What does it cost to use the dryer at Aldridge Hall, Tamsin Court, Innisfree Hall, Old Brewhouse, and Fenwick Court?", "rewritten": true, "history_turns": 1}, "output": {"answer": "Based on the provided documents:\n\n* **Tamsin Court:** The documents do not state a separate cost for the dryer, as it features an in-unit washer-dryer (housing_tamsin_court_laundry.txt and housing_tamsin_court.txt).\n* **Innisfree Hall:** The dryer costs $1.75 (housing_innisfree_hall.txt).\n* **Old Brewhouse:** The dryer costs $1.50 (housing_old_brewhouse.txt).\n* **Fenwick Court:** The dryer costs $1.75 (housing_fenwick_court_laundry.txt).\n\nI do not have enough information to answer for Aldridge Hall as it is not mentioned in the documents.", "sources": ["housing_fenwick_court_laundry.txt", "housing_innisfree_hall.txt", "housing_old_brewhouse.txt", "housing_tamsin_court.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 2639, "rewrite": 1780, "retrieve": 81, "generate": 777}, "retrieval": {"best_distance": 0.4299, "threshold": 0.6, "results": [{"source": "housing_old_brewhouse.txt", "distance": 0.4499}, {"source": "housing_innisfree_hall.txt", "distance": 0.4742}, {"source": "housing_fenwick_court_laundry.txt", "distance": 0.4299}, {"source": "housing_tamsin_court_laundry.txt", "distance": 0.6292}, {"source": "housing_tamsin_court.txt", "distance": 0.6291}]}, "usage": {"model_calls": 2, "cache_hits": 0, "tokens": {"prompt": 876, "output": 198, "total": 1074}, "tokens_by_stage": {"rewrite": {"prompt": 303, "output": 33, "total": 336}, "generate": {"prompt": 573, "output": 165, "total": 738}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": true, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
```

#### 2. Memory turns a scattered follow-up into a focused one

Same chain, turn 2 (`How much does it cost?`), memory off vs. on.

Memory **off**, session `cf4b2c288c64`, line 214. Best distance 0.5819, and
the answer covers laundry, printing and transcripts at once (sources include
`admin_printing_quota.txt` and `admin_transcript_requests.txt`):

```jsonl
{"schema": 1, "ts": "2026-11-16T04:16:50.945+00:00", "run_id": "31f9e63de572", "session_id": "cf4b2c288c64", "turn": 2, "source": "cli", "status": "ok", "input": {"question": "How much does it cost?", "standalone_question": "How much does it cost?", "rewritten": false, "history_turns": 0}, "output": {"answer": "Because your question does not specify what \"it\" refers to, here are the costs mentioned across the documents:\n\n* **Laundry:** $1.75 to wash and $1.75 to dry at Innisfree Hall (`housing_innisfree_hall.txt`); $1.50 to wash and $1.25 to dry at Morrow House (`housing_morrow_house.txt`); $2.00 to wash and $1.75 to dry at Calder Annexe (`housing_calder_annexe.txt`).\n* **Printing:** Every student gets $30 per semester, and colour costs eight times as much as black-and-white per page (`admin_printing_quota.txt`).\n* **Transcripts:** Official transcripts cost $8, while unofficial ones are free (`admin_transcript_requests.txt`).", "sources": ["admin_printing_quota.txt", "admin_transcript_requests.txt", "housing_calder_annexe.txt", "housing_innisfree_hall.txt", "housing_morrow_house.txt"]}, "duration_ms": {"total": 1139, "rewrite": 0, "retrieve": 122, "generate": 1017}, "retrieval": {"best_distance": 0.5819, "threshold": 0.6, "results": [{"source": "housing_innisfree_hall.txt", "distance": 0.6708}, {"source": "admin_printing_quota.txt", "distance": 0.6979}, {"source": "admin_transcript_requests.txt", "distance": 0.7395}, {"source": "housing_morrow_house.txt", "distance": 0.6788}, {"source": "housing_calder_annexe.txt", "distance": 0.5819}]}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 503, "output": 179, "total": 682}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}, "generate": {"prompt": 503, "output": 179, "total": 682}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": false, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
```

Memory **on** is line 217, shown under criterion 1 above. Best distance
0.3135, answer is laundry prices only, every source is `housing_*`.

- `retrieval` and `status` come from **`store.py::search`** and
  **`gate.py::check`**; `output.answer` from
  **`generate.py::answer_from_chunks`**, all called in `app.py::ask_pipeline`.

#### 3. Refusals are cheap and logged once

One session, `c2b368c95c4b`, lines 232–237: a warm-up question, then five
out-of-scope questions. Each refusal is one record with `model_calls: 0` and
79–120 ms, against 3330 ms for the answered warm-up.

- Refusal decided by **`gate.py::check`** (best distance over the 0.6 cutoff);
  the answer string is `gate.REFUSAL`, set in `app.py::ask_pipeline`, which
  returns before calling the model.

```jsonl
{"schema": 1, "ts": "2026-11-16T04:22:53.185+00:00", "run_id": "c84894d9ec5d", "session_id": "c2b368c95c4b", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "You can do laundry in the following locations, based on the provided documents:\n\n* Aldridge Hall (*housing_aldridge_hall_laundry.txt*)\n* Innisfree Hall (*housing_innisfree_hall_laundry.txt*)\n* Old Brewhouse (*housing_old_brewhouse_laundry.txt*)\n* Tamsin Court (*housing_tamsin_court_laundry.txt*)\n* Fenwick Court (*housing_fenwick_court_laundry.txt*)", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 3330, "rewrite": 0, "retrieve": 751, "generate": 2580}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6, "results": [{"source": "housing_aldridge_hall_laundry.txt", "distance": 0.4128}, {"source": "housing_innisfree_hall_laundry.txt", "distance": 0.3977}, {"source": "housing_old_brewhouse_laundry.txt", "distance": 0.3521}, {"source": "housing_tamsin_court_laundry.txt", "distance": 0.4502}, {"source": "housing_fenwick_court_laundry.txt", "distance": 0.4287}]}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 111, "total": 681}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}, "generate": {"prompt": 570, "output": 111, "total": 681}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": false, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
{"schema": 1, "ts": "2026-11-16T04:22:58.610+00:00", "run_id": "251fd7363aaf", "session_id": "c2b368c95c4b", "turn": 2, "source": "cli", "status": "refused", "input": {"question": "What is the capital of France?", "standalone_question": "What is the capital of France?", "rewritten": false, "history_turns": 0}, "output": {"answer": "I don't have enough information about that.", "sources": []}, "duration_ms": {"total": 92, "rewrite": 0, "retrieve": 91}, "retrieval": {"best_distance": 0.8587, "threshold": 0.6, "results": [{"source": "housing_innisfree_hall_noise.txt", "distance": 0.8606}, {"source": "housing_innisfree_hall.txt", "distance": 0.94}, {"source": "housing_fenwick_court_noise.txt", "distance": 0.8994}, {"source": "housing_innisfree_hall.txt", "distance": 0.9375}, {"source": "housing_tamsin_court.txt", "distance": 0.8587}]}, "usage": {"model_calls": 0, "cache_hits": 0, "tokens": {"prompt": 0, "output": 0, "total": 0}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": false, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
{"schema": 1, "ts": "2026-11-16T04:23:05.665+00:00", "run_id": "04fe9f9d5eb6", "session_id": "c2b368c95c4b", "turn": 3, "source": "cli", "status": "refused", "input": {"question": "How do I renew my passport?", "standalone_question": "How do I renew my passport?", "rewritten": false, "history_turns": 0}, "output": {"answer": "I don't have enough information about that.", "sources": []}, "duration_ms": {"total": 93, "rewrite": 0, "retrieve": 92}, "retrieval": {"best_distance": 0.8555, "threshold": 0.6, "results": [{"source": "course_biol_160.txt", "distance": 0.9894}, {"source": "course_cs_340.txt", "distance": 0.9291}, {"source": "course_cs_210.txt", "distance": 0.9894}, {"source": "admin_study_abroad.txt", "distance": 0.8572}, {"source": "course_engl_205_exams.txt", "distance": 0.8555}]}, "usage": {"model_calls": 0, "cache_hits": 0, "tokens": {"prompt": 0, "output": 0, "total": 0}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": false, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
{"schema": 1, "ts": "2026-11-16T04:23:13.112+00:00", "run_id": "de78d66ca26f", "session_id": "c2b368c95c4b", "turn": 4, "source": "cli", "status": "refused", "input": {"question": "What's the weather tomorrow?", "standalone_question": "What's the weather tomorrow?", "rewritten": false, "history_turns": 0}, "output": {"answer": "I don't have enough information about that.", "sources": []}, "duration_ms": {"total": 93, "rewrite": 0, "retrieve": 93}, "retrieval": {"best_distance": 0.656, "threshold": 0.6, "results": [{"source": "housing_innisfree_hall.txt", "distance": 0.8582}, {"source": "winter_gear.txt", "distance": 0.656}, {"source": "dining_the_atrium_followup.txt", "distance": 0.8628}, {"source": "dining_north_kitchen_followup.txt", "distance": 0.7763}, {"source": "dining_verrill_street_grill_followup.txt", "distance": 0.8291}]}, "usage": {"model_calls": 0, "cache_hits": 0, "tokens": {"prompt": 0, "output": 0, "total": 0}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": false, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
{"schema": 1, "ts": "2026-11-16T04:23:19.082+00:00", "run_id": "420f2bbbe3ba", "session_id": "c2b368c95c4b", "turn": 5, "source": "cli", "status": "refused", "input": {"question": "Who won the 2018 World Cup?", "standalone_question": "Who won the 2018 World Cup?", "rewritten": false, "history_turns": 0}, "output": {"answer": "I don't have enough information about that.", "sources": []}, "duration_ms": {"total": 120, "rewrite": 0, "retrieve": 120}, "retrieval": {"best_distance": 0.889, "threshold": 0.6, "results": [{"source": "course_hist_118_exams.txt", "distance": 0.9592}, {"source": "admin_study_abroad.txt", "distance": 0.889}, {"source": "course_hist_118.txt", "distance": 0.984}, {"source": "admin_housing_lottery.txt", "distance": 0.984}, {"source": "course_cs_210_exams.txt", "distance": 0.9667}]}, "usage": {"model_calls": 0, "cache_hits": 0, "tokens": {"prompt": 0, "output": 0, "total": 0}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": false, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
{"schema": 1, "ts": "2026-11-16T04:23:24.938+00:00", "run_id": "f585fbc97a29", "session_id": "c2b368c95c4b", "turn": 6, "source": "cli", "status": "refused", "input": {"question": "How do I file taxes?", "standalone_question": "How do I file taxes?", "rewritten": false, "history_turns": 0}, "output": {"answer": "I don't have enough information about that.", "sources": []}, "duration_ms": {"total": 79, "rewrite": 0, "retrieve": 79}, "retrieval": {"best_distance": 0.8581, "threshold": 0.6, "results": [{"source": "housing_fenwick_court_laundry.txt", "distance": 0.8581}, {"source": "housing_calder_annexe_laundry.txt", "distance": 0.8871}, {"source": "housing_old_brewhouse_laundry.txt", "distance": 0.8863}, {"source": "housing_innisfree_hall_laundry.txt", "distance": 0.8903}, {"source": "housing_aldridge_hall_laundry.txt", "distance": 0.8954}]}, "usage": {"model_calls": 0, "cache_hits": 0, "tokens": {"prompt": 0, "output": 0, "total": 0}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": false, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
```

#### 4. The cost of one run is measured

First batch of ten, `AI201_MEMORY=0`, `AI201_CACHE=0`, lines 244–253 (all 30
of my runs are also in `results/criterion4_3batches.jsonl`).

- `usage.tokens` is Gemini's own `usage_metadata`, summed by
  **`generate.py::_record_tokens`** and taken per run in
  `app.py::ask_pipeline` (`finish`).
- `usage.est_cost_usd` is from **`config.py::estimate_cost_usd`**.

```jsonl
{"schema": 1, "ts": "2026-11-16T04:24:54.586+00:00", "run_id": "882425528ed6", "session_id": "82f74e073301", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "Based on the provided documents, you can do laundry in the following locations:\n\n* Aldridge Hall (housing_aldridge_hall_laundry.txt)\n* Innisfree Hall (housing_innisfree_hall_laundry.txt)\n* Old Brewhouse (housing_old_brewhouse_laundry.txt)\n* Tamsin Court (housing_tamsin_court_laundry.txt)\n* Fenwick Court (housing_fenwick_court_laundry.txt)", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 3885, "rewrite": 0, "retrieve": 1046, "generate": 2839}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6, "results": [{"source": "housing_aldridge_hall_laundry.txt", "distance": 0.4128}, {"source": "housing_innisfree_hall_laundry.txt", "distance": 0.3977}, {"source": "housing_old_brewhouse_laundry.txt", "distance": 0.3521}, {"source": "housing_tamsin_court_laundry.txt", "distance": 0.4502}, {"source": "housing_fenwick_court_laundry.txt", "distance": 0.4287}]}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 111, "total": 681}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}, "generate": {"prompt": 570, "output": 111, "total": 681}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": false, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
{"schema": 1, "ts": "2026-11-16T04:24:59.288+00:00", "run_id": "4017ecdfcfa2", "session_id": "6993a644162b", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "You can do laundry in the following locations, according to the provided documents:\n\n* Aldridge Hall (housing_aldridge_hall_laundry.txt)\n* Innisfree Hall (housing_innisfree_hall_laundry.txt)\n* Old Brewhouse (housing_old_brewhouse_laundry.txt)\n* Tamsin Court (housing_tamsin_court_laundry.txt)\n* Fenwick Court (housing_fenwick_court_laundry.txt)", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 2982, "rewrite": 0, "retrieve": 750, "generate": 2231}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6, "results": [{"source": "housing_aldridge_hall_laundry.txt", "distance": 0.4128}, {"source": "housing_innisfree_hall_laundry.txt", "distance": 0.3977}, {"source": "housing_old_brewhouse_laundry.txt", "distance": 0.3521}, {"source": "housing_tamsin_court_laundry.txt", "distance": 0.4502}, {"source": "housing_fenwick_court_laundry.txt", "distance": 0.4287}]}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 111, "total": 681}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}, "generate": {"prompt": 570, "output": 111, "total": 681}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": false, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
{"schema": 1, "ts": "2026-11-16T04:25:03.881+00:00", "run_id": "fe11251a23e0", "session_id": "18f3a7480da4", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "Based on the provided documents, you can do laundry in the following locations:\n\n* Aldridge Hall (*housing_aldridge_hall_laundry.txt*)\n* Innisfree Hall (*housing_innisfree_hall_laundry.txt*)\n* Old Brewhouse (*housing_old_brewhouse_laundry.txt*)\n* Tamsin Court (*housing_tamsin_court_laundry.txt*)\n* Fenwick Court (*housing_fenwick_court_laundry.txt*)", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 2670, "rewrite": 0, "retrieve": 700, "generate": 1970}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6, "results": [{"source": "housing_aldridge_hall_laundry.txt", "distance": 0.4128}, {"source": "housing_innisfree_hall_laundry.txt", "distance": 0.3977}, {"source": "housing_old_brewhouse_laundry.txt", "distance": 0.3521}, {"source": "housing_tamsin_court_laundry.txt", "distance": 0.4502}, {"source": "housing_fenwick_court_laundry.txt", "distance": 0.4287}]}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 111, "total": 681}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}, "generate": {"prompt": 570, "output": 111, "total": 681}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": false, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
{"schema": 1, "ts": "2026-11-16T04:25:08.569+00:00", "run_id": "ff78dc3632f2", "session_id": "4213c6e34d43", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "Based on the provided documents, you can do laundry in the following locations:\n\n* Aldridge Hall (*housing_aldridge_hall_laundry.txt*)\n* Innisfree Hall (*housing_innisfree_hall_laundry.txt*)\n* Old Brewhouse (*housing_old_brewhouse_laundry.txt*)\n* Tamsin Court (*housing_tamsin_court_laundry.txt*)\n* Fenwick Court (*housing_fenwick_court_laundry.txt*)", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 2992, "rewrite": 0, "retrieve": 664, "generate": 2328}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6, "results": [{"source": "housing_aldridge_hall_laundry.txt", "distance": 0.4128}, {"source": "housing_innisfree_hall_laundry.txt", "distance": 0.3977}, {"source": "housing_old_brewhouse_laundry.txt", "distance": 0.3521}, {"source": "housing_tamsin_court_laundry.txt", "distance": 0.4502}, {"source": "housing_fenwick_court_laundry.txt", "distance": 0.4287}]}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 111, "total": 681}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}, "generate": {"prompt": 570, "output": 111, "total": 681}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": false, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
{"schema": 1, "ts": "2026-11-16T04:25:13.142+00:00", "run_id": "fb0e1925d1b1", "session_id": "f6572c8ba89a", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "Based on the provided documents, you can do laundry in the following locations:\n\n* Aldridge Hall (*housing_aldridge_hall_laundry.txt*)\n* Innisfree Hall (*housing_innisfree_hall_laundry.txt*)\n* Old Brewhouse (*housing_old_brewhouse_laundry.txt*)\n* Tamsin Court (*housing_tamsin_court_laundry.txt*)\n* Fenwick Court (*housing_fenwick_court_laundry.txt*)", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 2756, "rewrite": 0, "retrieve": 649, "generate": 2107}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6, "results": [{"source": "housing_aldridge_hall_laundry.txt", "distance": 0.4128}, {"source": "housing_innisfree_hall_laundry.txt", "distance": 0.3977}, {"source": "housing_old_brewhouse_laundry.txt", "distance": 0.3521}, {"source": "housing_tamsin_court_laundry.txt", "distance": 0.4502}, {"source": "housing_fenwick_court_laundry.txt", "distance": 0.4287}]}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 111, "total": 681}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}, "generate": {"prompt": 570, "output": 111, "total": 681}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": false, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
{"schema": 1, "ts": "2026-11-16T04:25:17.183+00:00", "run_id": "23f3b14d9b66", "session_id": "51006934de35", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "You can do laundry in the following locations based on the provided documents:\n- Aldridge Hall (*housing_aldridge_hall_laundry.txt*)\n- Innisfree Hall (*housing_innisfree_hall_laundry.txt*)\n- Old Brewhouse (*housing_old_brewhouse_laundry.txt*)\n- Tamsin Court (*housing_tamsin_court_laundry.txt*)\n- Fenwick Court (*housing_fenwick_court_laundry.txt*)", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 2442, "rewrite": 0, "retrieve": 634, "generate": 1808}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6, "results": [{"source": "housing_aldridge_hall_laundry.txt", "distance": 0.4128}, {"source": "housing_innisfree_hall_laundry.txt", "distance": 0.3977}, {"source": "housing_old_brewhouse_laundry.txt", "distance": 0.3521}, {"source": "housing_tamsin_court_laundry.txt", "distance": 0.4502}, {"source": "housing_fenwick_court_laundry.txt", "distance": 0.4287}]}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 110, "total": 680}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}, "generate": {"prompt": 570, "output": 110, "total": 680}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": false, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
{"schema": 1, "ts": "2026-11-16T04:25:21.939+00:00", "run_id": "e569215bd851", "session_id": "ee19b5f40e57", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "You can do laundry in the following locations, as stated in their respective documents:\n- Aldridge Hall (*housing_aldridge_hall_laundry.txt*)\n- Innisfree Hall (*housing_innisfree_hall_laundry.txt*)\n- Old Brewhouse (*housing_old_brewhouse_laundry.txt*)\n- Tamsin Court (*housing_tamsin_court_laundry.txt*)\n- Fenwick Court (*housing_fenwick_court_laundry.txt*)", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 2842, "rewrite": 0, "retrieve": 709, "generate": 2132}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6, "results": [{"source": "housing_aldridge_hall_laundry.txt", "distance": 0.4128}, {"source": "housing_innisfree_hall_laundry.txt", "distance": 0.3977}, {"source": "housing_old_brewhouse_laundry.txt", "distance": 0.3521}, {"source": "housing_tamsin_court_laundry.txt", "distance": 0.4502}, {"source": "housing_fenwick_court_laundry.txt", "distance": 0.4287}]}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 112, "total": 682}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}, "generate": {"prompt": 570, "output": 112, "total": 682}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": false, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
{"schema": 1, "ts": "2026-11-16T04:25:26.218+00:00", "run_id": "ac13e67f1148", "session_id": "6aceda71c734", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "You can do laundry in the following locations, according to their respective documents:\n* Aldridge Hall (`housing_aldridge_hall_laundry.txt`)\n* Innisfree Hall (`housing_innisfree_hall_laundry.txt`)\n* Old Brewhouse (`housing_old_brewhouse_laundry.txt`)\n* Tamsin Court (`housing_tamsin_court_laundry.txt`)\n* Fenwick Court (`housing_fenwick_court_laundry.txt`)", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 2708, "rewrite": 0, "retrieve": 669, "generate": 2039}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6, "results": [{"source": "housing_aldridge_hall_laundry.txt", "distance": 0.4128}, {"source": "housing_innisfree_hall_laundry.txt", "distance": 0.3977}, {"source": "housing_old_brewhouse_laundry.txt", "distance": 0.3521}, {"source": "housing_tamsin_court_laundry.txt", "distance": 0.4502}, {"source": "housing_fenwick_court_laundry.txt", "distance": 0.4287}]}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 111, "total": 681}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}, "generate": {"prompt": 570, "output": 111, "total": 681}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": false, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
{"schema": 1, "ts": "2026-11-16T04:25:31.113+00:00", "run_id": "2fba919a7157", "session_id": "5119c5836a71", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "You can do laundry in the following locations, according to their respective documents:\n- Aldridge Hall (*housing_aldridge_hall_laundry.txt*)\n- Innisfree Hall (*housing_innisfree_hall_laundry.txt*)\n- Old Brewhouse (*housing_old_brewhouse_laundry.txt*)\n- Tamsin Court (*housing_tamsin_court_laundry.txt*)\n- Fenwick Court (*housing_fenwick_court_laundry.txt*)", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 3333, "rewrite": 0, "retrieve": 690, "generate": 2643}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6, "results": [{"source": "housing_aldridge_hall_laundry.txt", "distance": 0.4128}, {"source": "housing_innisfree_hall_laundry.txt", "distance": 0.3977}, {"source": "housing_old_brewhouse_laundry.txt", "distance": 0.3521}, {"source": "housing_tamsin_court_laundry.txt", "distance": 0.4502}, {"source": "housing_fenwick_court_laundry.txt", "distance": 0.4287}]}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 111, "total": 681}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}, "generate": {"prompt": 570, "output": 111, "total": 681}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": false, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
{"schema": 1, "ts": "2026-11-16T04:25:35.911+00:00", "run_id": "a3c56907d368", "session_id": "b492d79bf19e", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "Based on the provided documents, you can do laundry in the following locations:\n\n* Aldridge Hall (housing_aldridge_hall_laundry.txt)\n* Innisfree Hall (housing_innisfree_hall_laundry.txt)\n* Old Brewhouse (housing_old_brewhouse_laundry.txt)\n* Tamsin Court (housing_tamsin_court_laundry.txt)\n* Fenwick Court (housing_fenwick_court_laundry.txt)", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 3111, "rewrite": 0, "retrieve": 689, "generate": 2422}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6, "results": [{"source": "housing_aldridge_hall_laundry.txt", "distance": 0.4128}, {"source": "housing_innisfree_hall_laundry.txt", "distance": 0.3977}, {"source": "housing_old_brewhouse_laundry.txt", "distance": 0.3521}, {"source": "housing_tamsin_court_laundry.txt", "distance": 0.4502}, {"source": "housing_fenwick_court_laundry.txt", "distance": 0.4287}]}, "usage": {"model_calls": 1, "cache_hits": 0, "tokens": {"prompt": 570, "output": 111, "total": 681}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}, "generate": {"prompt": 570, "output": 111, "total": 681}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "default", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": false, "cache": false, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
```

#### 5. The variant index is auditable

Building the `v2` index, scripted run 1 (`results/final_runs/run1/c5_index_v2.txt`),
printed by **`app.py::cmd_index`**, which chunks with
`chunker.py::split_documents`, summarises with `chunker.py::describe` and stores
with **`store.py::build_index`**:

```text
$ AI201_CACHE=0 AI201_MEMORY=1 python app.py --corpus campus_life --variant v2 index
# exit code: 0

Corpus: campus_life
  loaded   88 documents, 27,908 characters, ~317 characters per document
  chunked  91 chunks, 307 characters on average (shortest 159, longest 430), produced by chunker.py::split_documents
  embedding 91 chunks (first run downloads the model)...
  stored   91 chunks in 5.9s

Ready. Try: python app.py ask "your question here"
```

The chunk listing, scripted run 1 (`results/final_runs/run1/c5_chunks_laundry.txt`),
printed by **`app.py::cmd_chunks`**. The `produced by` label is set in
**`chunker.py::split_documents`**:

```text
$ AI201_CACHE=0 AI201_MEMORY=1 python app.py --corpus campus_life chunks --from-doc housing_aldridge_hall_laundry
# exit code: 0

91 chunks total. Showing all 1 from housing_aldridge_hall_laundry.txt.

Paste these into your README under Sample Chunks. The rubric asks
for the source file and the function that produced them — both are
printed for you below.

======================================================================
Chunk 1  |  source: housing_aldridge_hall_laundry.txt#0  |  produced by: chunker.py::split_documents
======================================================================
Laundry in Aldridge Hall

Machines take $1.75 wash, $1.50 dry, card only. There are eight washers and six dryers for the building, which is the wrong ratio and means the dryers back up on Sunday evenings.

Best time to do laundry here is Tuesday or Wednesday morning. Sunday after 6pm you will wait.

For each one, ask: could someone answer a question using only this,
without reading what came before or after?
```

An ask against the `v2` index from my terminal, line 274. `settings.variant` is
`"v2"`. This one was a cache hit (`cache: true`, `model_calls: 0`):

```jsonl
{"schema": 1, "ts": "2026-11-16T04:28:33.653+00:00", "run_id": "66b1647965da", "session_id": "4f301b6f0fec", "turn": 1, "source": "cli", "status": "ok", "input": {"question": "Where can I do laundry?", "standalone_question": "Where can I do laundry?", "rewritten": false, "history_turns": 0}, "output": {"answer": "Based on the provided documents, you can do laundry in the following locations:\n- Aldridge Hall (*housing_aldridge_hall_laundry.txt*)\n- Innisfree Hall (*housing_innisfree_hall_laundry.txt*)\n- Old Brewhouse (*housing_old_brewhouse_laundry.txt*)\n- Tamsin Court (*housing_tamsin_court_laundry.txt*)\n- Fenwick Court (*housing_fenwick_court_laundry.txt*)", "sources": ["housing_aldridge_hall_laundry.txt", "housing_fenwick_court_laundry.txt", "housing_innisfree_hall_laundry.txt", "housing_old_brewhouse_laundry.txt", "housing_tamsin_court_laundry.txt"]}, "duration_ms": {"total": 802, "rewrite": 0, "retrieve": 801, "generate": 1}, "retrieval": {"best_distance": 0.3521, "threshold": 0.6, "results": [{"source": "housing_aldridge_hall_laundry.txt", "distance": 0.4128}, {"source": "housing_innisfree_hall_laundry.txt", "distance": 0.3977}, {"source": "housing_old_brewhouse_laundry.txt", "distance": 0.3521}, {"source": "housing_tamsin_court_laundry.txt", "distance": 0.4502}, {"source": "housing_fenwick_court_laundry.txt", "distance": 0.4287}]}, "usage": {"model_calls": 0, "cache_hits": 1, "tokens": {"prompt": 0, "output": 0, "total": 0}, "tokens_by_stage": {"rewrite": {"prompt": 0, "output": 0, "total": 0}, "generate": {"prompt": 0, "output": 0, "total": 0}}, "est_cost_usd": 0.0}, "settings": {"corpus": "campus_life", "variant": "v2", "model": "gemini-3.5-flash-lite", "embedding_model": "all-MiniLM-L6-v2", "top_k": 5, "hybrid": true, "memory": false, "cache": true, "price_input_per_m": 0.0, "price_output_per_m": 0.0}}
```
