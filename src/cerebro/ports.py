"""Portas para os componentes que fazem I/O ou carregam modelo."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Protocol

from cerebro.models import Chunk, Hit, MetadataValue


class Encoder(Protocol):
    dimension: int

    def encode(self, texts: Sequence[str]) -> list[list[float]]: ...


class VectorStore(Protocol):
    def upsert(self, chunks: Sequence[Chunk], vectors: Sequence[Sequence[float]]) -> None: ...

    def delete_sources(self, source_ids: Sequence[str]) -> None: ...

    def search(self, vector: Sequence[float], limit: int, where: Mapping[str, MetadataValue]) -> list[Hit]: ...


class Reranker(Protocol):
    def rerank(self, question: str, hits: Sequence[Hit], top: int) -> list[Hit]: ...


class Generator(Protocol):
    def generate(self, prompt: str) -> str: ...
