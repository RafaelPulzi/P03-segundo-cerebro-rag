"""Recuperação lexical com BM25."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from cerebro.models import Chunk, Hit, MetadataValue


class Bm25Index:
    """Pega o que a busca densa perde: siglas e nomes próprios (P90, k3s, Longhorn)."""

    def __init__(self, chunks: Sequence[Chunk]) -> None:
        self._chunks = tuple(chunks)

    def search(self, question: str, limit: int, where: Mapping[str, MetadataValue]) -> list[Hit]:
        raise NotImplementedError("Fase 3")
