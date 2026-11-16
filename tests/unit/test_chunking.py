"""Chunking de nota (RF-02, cenário C1)."""

from __future__ import annotations

from cerebro.chunk.notes import split_note
from cerebro.models import Document

NOTE = Document(
    source_id="P99.md",
    kind="note",
    title="P99 - Projeto de Teste",
    text="# P99\n\nIntrodução.\n\n## Arquitetura\n\nUm Raspberry Pi.\n\n## Roadmap\n\n1. Ligar.\n",
    metadata={"difficulty": "03Hard"},
    content_hash="h",
)


def test_one_chunk_per_heading_with_trail_as_context() -> None:
    chunks = split_note(NOTE, max_tokens=800)
    assert [chunk.context for chunk in chunks] == ["P99", "P99 › Arquitetura", "P99 › Roadmap"]


def test_chunks_inherit_frontmatter() -> None:
    assert all(chunk.metadata["difficulty"] == "03Hard" for chunk in split_note(NOTE, max_tokens=800))


def test_long_section_splits_by_paragraph_keeping_context() -> None:
    long_note = NOTE.model_copy(update={"text": "## Longa\n\n" + "\n\n".join(["palavra " * 200] * 3)})
    chunks = split_note(long_note, max_tokens=300)
    assert len(chunks) >= 3
    assert {chunk.context for chunk in chunks} == {"P99 - Projeto de Teste › Longa"}
