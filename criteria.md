# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
One of my questions is about a topic only two documents mention, so
     I expect that one to be hard."

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
Why 5/5 and not 4/5: Citation is a deterministic formatting step, not a probabilistic retrieval outcome — if my code passes source metadata through to the output layer, every answer is guaranteed a source, so a single miss signals a bug rather than acceptable variance.

What makes it achievable / what would break it: My pipeline attaches source metadata to every chunk at index time and carries it through retrieval, so 5/5 holds unless metadata is dropped during chunking, lost between index and retrieval, or the relevance gate blocks an answer without a fallback citation policy

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into run log.  -->

**Why this target:**
The relevance gate compares distances to a numeric cutoff, and that cutoff sits in a fuzzy boundary zone where in-scope and out-of-scope questions can overlap — so one borderline case slipping through is expected. Requiring 5/5 would force the cutoff so low that legitimate questions get refused.

Why 4/5: The relevance cutoff operates on a continuous distance scale where in-scope and out-of-scope questions can overlap near the boundary. In my data, in-scope questions scored 0.35–0.58 and out-of-scope scored 0.68–0.89, leaving a gap of roughly 0.10. Because one in-scope question landed at 0.58 (close to the boundary), requiring 5/5 would force a cutoff low enough to refuse legitimate questions — a worse failure than allowing one borderline miss.

Distance analysis: I set the cutoff at 0.62, inside the gap. The two groups were mostly separated but not perfectly — one in-scope question and one out-of-scope question came within 0.10 of each other, confirming that a thin overlap is inherent to the corpus.

---

## 4. Something about your chunks

At least 4 of 5 sampled chunks hold together as one self-contained idea — starting and ending at a natural boundary rather than mid-sentence — and every chunk is long enough (≥200 characters) to stand on its own.

**Why this target:**
The starter merged multiple natural units into single thread-level chunks, so "right size" has two observable signals: each chunk must be self-contained (no severed sentences) and must clear a minimum length floor


---

## 5. Your choice

when ask same questions 3 times, 4 of 5 questions return the same core chunks in all 3 runs, and answers are semantically equivalent


**Why this target:**
Make sure the stability, minor shuffling at the bottom of the top-k is expected and harmless; what matters is that the answer-bearing chunk appears every time and the final answer means the same thing, even if phrased differently.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
