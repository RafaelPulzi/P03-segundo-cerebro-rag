"""Contratos do pipeline."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from cerebro.models import Chunk


def test_embedding_text_prefixes_context() -> None:
    chunk = Chunk(chunk_id="a#1", source_id="a.md", text="Um Raspberry Pi.", context="P99 › Arquitetura")
    assert chunk.embedding_text == "P99 › Arquitetura\n\nUm Raspberry Pi."


def test_embedding_text_without_context_is_the_text() -> None:
    assert Chunk(chunk_id="a#1", source_id="a.md", text="texto", context="").embedding_text == "texto"


def test_chunk_is_immutable() -> None:
    chunk = Chunk(chunk_id="a#1", source_id="a.md", text="t", context="c")
    with pytest.raises(ValidationError):
        chunk.text = "outro"  # type: ignore[misc]
