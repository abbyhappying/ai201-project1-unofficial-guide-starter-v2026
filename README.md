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

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2


## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

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

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
