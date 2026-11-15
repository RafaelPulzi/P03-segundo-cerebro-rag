"""Recuperação híbrida de ponta a ponta."""

from __future__ import annotations

from collections.abc import Mapping

from cerebro.models import Hit, MetadataValue
from cerebro.ports import Encoder, Reranker, VectorStore
from cerebro.retrieve.bm25 import Bm25Index


class HybridRetriever:
    def __init__(
        self, encoder: Encoder, store: VectorStore, lexical: Bm25Index, reranker: Reranker | None, rrf_k: int
    ) -> None:
        self._encoder = encoder
        self._store = store
        self._lexical = lexical
        self._reranker = reranker
        self._rrf_k = rrf_k

    def retrieve(self, question: str, where: Mapping[str, MetadataValue], candidates: int, top: int) -> list[Hit]:
        raise NotImplementedError("Fase 3")
