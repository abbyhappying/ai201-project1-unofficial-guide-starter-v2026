"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document

# Ceiling for merging paragraphs in the unstructured branch (campus_life).
#
# Measured against that corpus: 183 bare paragraphs is too granular — median
# body is 112 characters and the shortest is 36 — while a ceiling of 600 or
# more swallows every document whole and reproduces the baseline's 88 chunks.
MERGE_TARGET = 450


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks



def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents on their own structure rather than on a character count.

    Which structure depends on what the document has, because the two corpora
    are shaped differently and one function serves whichever `config.CORPUS`
    points at:

      - Markdown with '##' headings (city_guides) is cut at those headings.
        All 14 guides share near-identical section names — "Getting there",
        "Getting around", "Where to stay" — so the '#' title is prepended to
        every chunk. Without it, fourteen "Getting there" sections embed
        almost identically and retrieval for a named town is a coin flip.

      - Everything else (campus_life) is cut at paragraph breaks, with short
        paragraphs merged up to MERGE_TARGET and the title prepended. The
        documents are short, median 324 characters, but they bundle unrelated
        facts: housing_old_brewhouse.txt covers build history, heating,
        laundry prices and acoustics in one piece.

    CHUNK_SIZE is a backstop here, not a tuning parameter: it only fires if a
    natural section is somehow longer than it, which on these corpora never
    happens. CHUNK_OVERLAP goes unused — chunks end at structural boundaries,
    so there is no severed sentence for an overlap to repair.
    """
    heading_re = re.compile(r"^##+\s+(.*)$", re.M)
    chunks: list[Chunk] = []

    for doc in documents:
        # The title is the first line, minus any leading '#'.
        title, _, body = doc.text.partition("\n")
        title = title.strip().lstrip("#").strip()

        # The city_guides files are hard-wrapped at about 80 columns, so a
        # single newline is a display artefact rather than a boundary — one
        # sentence in guide_accessibility.md spans four lines. Rejoin those,
        # drop Markdown emphasis, and keep blank lines as paragraph breaks.
        blocks = [
            " ".join(line.strip() for line in block.split("\n") if line.strip())
            for block in body.split("\n\n")
        ]
        body = "\n\n".join(b.replace("**", "") for b in blocks if b)

        pieces: list[str] = []

        if heading_re.search(body):
            # ── city_guides: cut at '##' headings ────────────────────────────
            # Text before the first heading (the standing intro in
            # guide_accessibility.md, for instance) is kept, not dropped.
            heading: str | None = None
            position = 0
            sections: list[tuple[str | None, str]] = []

            for match in heading_re.finditer(body):
                segment = body[position : match.start()].strip()
                if segment:
                    sections.append((heading, segment))
                heading = match.group(1).strip()
                position = match.end()

            tail = body[position:].strip()
            if tail:
                sections.append((heading, tail))

            for heading, section in sections:
                label = f"{title} — {heading}" if heading else title
                pieces.append(f"{label}\n\n{section}")

        else:
            # ── campus_life: cut at paragraph breaks, merging short ones ─────
            # The ceiling counts the title prefix too, so it applies to the
            # finished chunk. It is a stopping rule, not a target: nothing is
            # padded, and a paragraph that would overshoot starts a new chunk.
            reserved = len(title) + 2
            current = ""

            for para in (p.strip() for p in body.split("\n\n")):
                if not para:
                    continue
                if current and reserved + len(current) + len(para) + 2 > MERGE_TARGET:
                    pieces.append(f"{title}\n\n{current}")
                    current = para
                else:
                    current = f"{current}\n\n{para}" if current else para

            if current:
                pieces.append(f"{title}\n\n{current}")

        # A document with nothing under its title still has to be indexed.
        if not pieces and title:
            pieces = [title]

        index = 0
        for piece in pieces:
            # The backstop. Cuts at sentence ends so an over-long document
            # dropped into corpora/ degrades into sentence-aligned pieces
            # rather than one oversized chunk.
            parts = [piece]
            if len(piece) > config.CHUNK_SIZE:
                parts, current = [], ""
                for sentence in re.split(r"(?<=[.!?])\s+", piece):
                    if current and len(current) + len(sentence) + 1 > config.CHUNK_SIZE:
                        parts.append(current)
                        current = sentence
                    else:
                        current = f"{current} {sentence}" if current else sentence
                    while len(current) > config.CHUNK_SIZE:  # one huge sentence
                        parts.append(current[: config.CHUNK_SIZE])
                        current = current[config.CHUNK_SIZE :]
                if current:
                    parts.append(current)

            for part in parts:
                part = part.strip()
                if not part:
                    continue
                chunks.append(
                    Chunk(
                        text=part,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )
                index += 1

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
