"""
Your test questions.

Milestone 2 asks you to write five questions your system should be able to
answer from your corpus, specific enough to have a right answer.

  ✗ "What are good dining halls?"          — no right answer
  ✓ "What do students say about wait times at Commons during lunch?"

Fill in `QUESTIONS` below. `expects` is a word or short phrase you'd expect a
correct answer to contain — you'll use it in unit 2 when you build a scorer,
and having written it now means you decided what "correct" meant before you saw
any results.

`OUT_OF_SCOPE` holds five questions your documents clearly don't cover. You
need these in Milestone 4 to find where your relevance cutoff belongs, and
again in unit 2, where `run_eval.py` runs them through the gate and writes what
happened into your run log — that's the evidence for criterion 3.

Swap them for your own if you like. Keep five of them either way: criterion 3
names a target of "4 of 5", and four of three is not a thing.
"""

# Corpus: city_guides — nine town guides plus five cross-cutting guides
# (eating, walking, seasons, regional transport, accessibility).
#
# Criterion 1 in criteria.md targets 4 of 5 and says one question is about a
# topic only two documents mention. That question is the last one below: the
# Elder Ness tidal flooding appears in guide_elder_ness.md and guide_walking.md
# and nowhere else. The other four each sit in three or more documents, because
# a fact stated in both a town guide and a cross-cutting guide gives retrieval
# more than one chunk that can carry the answer.
QUESTIONS = [
    # guide_eating.md, guide_marchwood.md, guide_kestrelford.md,
    # guide_brightwater.md — the region-wide 9pm rule and its one exception.
    {
        "question": "If I want to eat dinner at 9:30pm, which town in the "
                    "region can I actually get a hot meal in?",
        "expects": "Marchwood",
    },
    # guide_halden_bay.md, guide_regional_transport.md, guide_seasons.md —
    # all three give the same arrival time.
    {
        "question": "How early do I need to arrive in Halden Bay to find "
                    "parking on a summer weekend?",
        "expects": "10am",
    },
    # guide_walking.md, guide_kestrelford.md, guide_regional_transport.md —
    # all three call the trackbed the best walking for the effort.
    {
        "question": "Which walking route in the region gives the most for the "
                    "least effort, and how long is it?",
        "expects": "six miles",
    },
    # guide_accessibility.md, guide_thornby_wells.md, guide_walking.md — named
    # the easiest town in all three.
    {
        "question": "Which town in the region is easiest to get around with "
                    "limited mobility?",
        "expects": "Thornby Wells",
    },
    # HARD (two documents only): guide_elder_ness.md and guide_walking.md.
    {
        "question": "How often does the access road to Elder Ness flood, and "
                    "for how long each time?",
        "expects": "six times a year",
    },
]

# Questions from a different world entirely. Your gate should refuse all five.
#
# There are five of these because criterion 3 in criteria.md names a target of
# "at least 4 of 5" — you need five things to try before you can report 4 of 5.
# `run_eval.py` runs these through retrieval and the gate on every eval and
# records what happened, so criterion 3 has evidence in the run log alongside
# the others. They cost no model calls: a refusal never reaches the model.
OUT_OF_SCOPE = [
    "What is the capital of Mongolia?",
    "How do I change the oil in a diesel engine?",
    "Who won the 1994 World Cup?",
    "What is the recommended dosage of ibuprofen for a headache?",
    "How do I write a for loop in Rust?",
]


def answered() -> list[dict]:
    """The questions you've actually filled in."""
    return [q for q in QUESTIONS if q.get("question", "").strip()]
