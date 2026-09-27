"""
Stages 3 and 4 of the pipeline: embedding chunks and retrieving them.

Three things in here are worth knowing about, because they'd quietly break the
rest of the project if they were wrong:

1. The Chroma collection is created with cosine distance, explicitly. Chroma
   defaults to squared L2, and the 0.6 threshold the course uses is calibrated
   against cosine. Getting this wrong makes every distance number meaningless.

2. `search` returns the distance alongside each chunk. Milestone 4 has you
   compare distances, so they have to be visible.

3. The embedding model is the one Chroma bundles, not one loaded through
   `sentence-transformers`. It is the same model — `all-MiniLM-L6-v2`, 384
   dimensions — but it arrives as an ONNX build from Chroma's own CDN, so the
   install needs neither PyTorch nor a reachable Hugging Face. See `_embedder`.

4. When `config.HYBRID` is on, `search` runs a keyword search beside the vector
   search and merges the two rankings — see `_fuse`. `Result.distance` keeps
   meaning cosine distance either way, because the relevance gate reads it.
"""

import os
import re
import shutil
from dataclasses import dataclass

# Must be set BEFORE chromadb is imported. Without it, some Chroma versions
# print "Failed to send telemetry event ..." on every single call — which looks
# exactly like a real error, isn't one, and cost a previous cohort a lot of
# confused help-channel messages.
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

import chromadb  # noqa: E402

import config
from chunker import Chunk


@dataclass
class Result:
    """One retrieved chunk and how far it was from the question."""

    text: str
    source: str
    label: str
    distance: float   # LOWER IS BETTER. 0.3 is close, 0.9 is unrelated.
    produced_by: str


_model = None

# The model Chroma bundles. Anything else in config.EMBEDDING_MODEL means
# "fetch that one from Hugging Face instead" — see `_embedder`.
BUNDLED_MODEL = "all-MiniLM-L6-v2"


class _OnnxEmbedder:
    """
    Chroma's built-in embedder, wrapped to look like the other two.

    Chroma's embedding functions are called directly and hand back numpy
    arrays. The rest of this file wants `.encode(texts)`, so the adapter lives
    here rather than making every caller care which embedder it got.
    """

    def __init__(self):
        from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2

        self._ef = ONNXMiniLM_L6_V2()

    def encode(self, texts, show_progress_bar: bool = False):
        return [vector.tolist() for vector in self._ef(list(texts))]


def _sentence_transformer(name: str):
    """
    The escape hatch: any model that isn't the bundled one.

    Unit 2's "try a second embedding model" stretch option comes through here,
    and so does anything you set `EMBEDDING_MODEL` to. This path *does* need
    `sentence-transformers` and a reachable Hugging Face, neither of which the
    default install has — which is the whole point of the default install.
    """
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError(
            f"config.EMBEDDING_MODEL is set to {name!r}, which isn't the model "
            f"Chroma bundles ({BUNDLED_MODEL!r}), so it has to be downloaded "
            f"from Hugging Face.\n"
            f"Install the optional dependency first:\n"
            f"    pip install 'sentence-transformers>=3.4,<3.5'\n"
            f"Or set EMBEDDING_MODEL back to {BUNDLED_MODEL!r}."
        ) from exc

    return SentenceTransformer(name)


def _embedder():
    """
    Load the embedding model once and keep it.

    First call is slow — it downloads about 80 MB. That's why setup happens
    before class.
    """
    global _model

    if _model is not None:
        return _model

    # Used only by this repo's own smoke test, which runs where no model can be
    # downloaded at all. Never set this yourself.
    if os.getenv("AI201_FAKE_EMBEDDINGS") == "1":
        from _smoke_embedder import FakeEmbedder

        _model = FakeEmbedder()
    elif config.EMBEDDING_MODEL == BUNDLED_MODEL:
        _model = _OnnxEmbedder()
    else:
        _model = _sentence_transformer(config.EMBEDDING_MODEL)

    return _model


def embed(texts: list[str]) -> list[list[float]]:
    """Turn text into vectors. Runs on your machine, costs no API quota."""
    vectors = _embedder().encode(texts, show_progress_bar=False)
    # sentence-transformers and the smoke stand-in return something with a
    # .tolist(); _OnnxEmbedder has already done that conversion itself.
    return vectors.tolist() if hasattr(vectors, "tolist") else vectors


def _client():
    return chromadb.PersistentClient(
        path=str(config.CHROMA_DIR),
        settings=chromadb.config.Settings(anonymized_telemetry=False),
    )


def build_index(
    chunks: list[Chunk],
    corpus: str | None = None,
    variant: str = "default",
) -> int:
    """
    Embed every chunk and store it.

    `variant` lets you keep more than one index of the same corpus at the same
    time. In unit 2, when you compare two chunking strategies, index the second
    one as variant="v2" and you can query both instead of deleting the first
    and starting over.
    """
    name = config.collection_name(corpus, variant)
    client = _client()

    # These chunks are about to be replaced, so any keyword index built from
    # the old ones is now wrong. Without this line, re-chunking and re-indexing
    # would leave the keyword half of `search` answering from the chunks you
    # just deleted, for as long as the process stayed alive.
    _bm25_cache.pop(name, None)

    try:
        client.delete_collection(name)
    except Exception:
        pass

    collection = client.create_collection(
        name=name,
        # ⚠️ Do not remove. Chroma defaults to squared L2, and every distance
        # number in this course assumes cosine.
        metadata={"hnsw:space": "cosine"},
    )

    batch = 256
    for start in range(0, len(chunks), batch):
        window = chunks[start : start + batch]
        collection.add(
            ids=[f"{c.source}#{c.index}" for c in window],
            documents=[c.text for c in window],
            embeddings=embed([c.text for c in window]),
            metadatas=[
                {"source": c.source, "index": c.index, "produced_by": c.produced_by}
                for c in window
            ],
        )

    return len(chunks)


# How much a chunk's position in one ranking is worth when the two rankings
# are merged: 1 / (RRF_K + rank). The standard 60 is deliberately flat, so a
# chunk both searches liked beats a chunk only one of them liked. Lower it to
# make being *first* in one ranking count for more.
RRF_K = 60

# One BM25 index per collection, built on first use. Dropped in `build_index`
# and `reset`, because both change the chunks underneath it.
_bm25_cache: dict[str, tuple] = {}


def _tokens(text: str) -> list[str]:
    """Words and numbers, lowercased.

    No stemming and no stopword list: BM25 weights a word by how rare it is,
    so "the" is already worth almost nothing without a list to say so.
    """
    return re.findall(r"\w+", text.lower())


def _bm25_index(collection, name: str):
    """A keyword index over the chunks Chroma is already holding.

    The text comes back out of the same collection the vectors are in, so
    there is no second index file to build, ship or keep in step — and no way
    for the two searches to end up looking at different chunks.
    """
    if name not in _bm25_cache:
        from rank_bm25 import BM25Okapi

        stored = collection.get(include=["documents", "metadatas"])
        labels = [
            f"{meta.get('source', 'unknown')}#{meta.get('index', 0)}"
            for meta in stored["metadatas"]
        ]
        index = BM25Okapi([_tokens(document) for document in stored["documents"]])
        _bm25_cache[name] = (index, labels)

    return _bm25_cache[name]


def _fuse(
    question: str,
    results: list[Result],
    collection,
    name: str,
    top_k: int,
) -> list[Result]:
    """
    Merge the vector ranking with a keyword ranking and keep the best `top_k`.

    Reciprocal Rank Fusion: a chunk scores 1 / (RRF_K + rank) in each ranking
    and the two are added. Note that this reads only the ORDER each search put
    things in, never the numbers. That is the point — a cosine distance runs 0
    to 2 and a BM25 score has no ceiling at all, so adding them directly is
    meaningless, and rescaling them to fit would make the best hit of every
    question look equally good, including the questions with no answer in the
    corpus at all.
    """
    bm25, labels = _bm25_index(collection, name)
    scores = bm25.get_scores(_tokens(question))

    by_score = sorted(range(len(labels)), key=lambda i: -scores[i])
    keyword_rank = {labels[i]: rank for rank, i in enumerate(by_score, 1)}
    vector_rank = {result.label: rank for rank, result in enumerate(results, 1)}
    unranked = len(labels) + 1      # for anything one of the two never saw

    def fused(result: Result) -> float:
        return 1 / (RRF_K + vector_rank.get(result.label, unranked)) + 1 / (
            RRF_K + keyword_rank.get(result.label, unranked)
        )

    top = sorted(results, key=fused, reverse=True)[:top_k]

    # gate.py refuses when the smallest distance among these is over
    # THRESHOLD, and that cutoff was calibrated against vector search alone.
    # Merging re-orders, so the nearest chunk can land outside top_k — and the
    # gate would start refusing questions it used to answer, for no reason it
    # could show you. Putting it back means the gate sees the same number it
    # saw before. Throwing away the closest chunk was never a good idea anyway.
    if results and top and results[0] not in top:
        top[-1] = results[0]

    return top


def search(
    question: str,
    top_k: int | None = None,
    corpus: str | None = None,
    variant: str = "default",
) -> list[Result]:
    """
    Retrieve the chunks closest in meaning to a question.

    Returns them nearest-first, each with its distance — unless
    `config.HYBRID` is on, in which case a keyword search has had a say in the
    order too and the distances no longer only ever go up. They are still real
    cosine distances; see `_fuse`.
    """
    top_k = top_k or config.TOP_K
    name = config.collection_name(corpus, variant)

    try:
        collection = _client().get_collection(name)
    except Exception as exc:
        raise RuntimeError(
            f"No index called '{name}'. Run `python app.py index` first."
        ) from exc

    # Merging two rankings is easiest when both cover the same chunks, so the
    # hybrid path asks for all of them. At this corpus size — 94 chunks — that
    # costs nothing and removes a knob nobody would know how to tune. If you
    # ever point this at thousands of chunks, ask for a few hundred here
    # instead: the merge itself doesn't change.
    count = collection.count()
    raw = collection.query(
        query_embeddings=embed([question]),
        n_results=count if config.HYBRID else min(top_k, count),
    )

    results: list[Result] = []
    for text, meta, distance in zip(
        raw["documents"][0], raw["metadatas"][0], raw["distances"][0]
    ):
        results.append(
            Result(
                text=text,
                source=str(meta.get("source", "unknown")),
                label=f"{meta.get('source', 'unknown')}#{meta.get('index', 0)}",
                distance=float(distance),
                produced_by=str(meta.get("produced_by", "unknown")),
            )
        )

    if not config.HYBRID:
        return results

    return _fuse(question, results, collection, name, top_k)


def index_exists(corpus: str | None = None, variant: str = "default") -> bool:
    """Is there an index here to search, without searching it?

    `serve.py`'s health check asks this. It deliberately does not embed
    anything: loading the embedding model takes 80 MB and a few seconds, and a
    health check that heavy is a health check nobody can afford to call.
    """
    try:
        collection = _client().get_collection(config.collection_name(corpus, variant))
        return collection.count() > 0
    except Exception:
        return False


def reset():
    """Delete every index. Occasionally the fastest way out of a mess."""
    _bm25_cache.clear()
    if config.CHROMA_DIR.exists():
        shutil.rmtree(config.CHROMA_DIR)
