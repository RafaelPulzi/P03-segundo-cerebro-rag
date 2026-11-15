"""Chunking de nota do vault (ADR 0001)."""

from __future__ import annotations

from cerebro.models import Chunk, Document


def split_note(document: Document, max_tokens: int) -> list[Chunk]:
    """Um chunk por heading (``#``, ``##``, ``###``).

    ``context`` é a trilha ``Título › H2 › H3``. Seção maior que ``max_tokens`` (estimado como
    palavras × 1,3) quebra por parágrafo mantendo o mesmo ``context``. Bloco de código não é
    cortado no meio.
    """
    raise NotImplementedError("Fase 1")
