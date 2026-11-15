"""Armazenamento vetorial no Qdrant."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from cerebro.models import Chunk, Hit, MetadataValue


class QdrantStore:
    """Cria a coleção na primeira escrita com índice de payload para ``difficulty``, ``project_status`` e ``tags``."""

    def __init__(self, url: str, collection: str, dimension: int) -> None:
        self._url = url
        self._collection = collection
        self._dimension = dimension

    def upsert(self, chunks: Sequence[Chunk], vectors: Sequence[Sequence[float]]) -> None:
        raise NotImplementedError("Fase 2")

    def delete_sources(self, source_ids: Sequence[str]) -> None:
        raise NotImplementedError("Fase 2")

    def search(self, vector: Sequence[float], limit: int, where: Mapping[str, MetadataValue]) -> list[Hit]:
        raise NotImplementedError("Fase 2")
