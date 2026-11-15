"""Modelos locais via sentence-transformers (extra ``modelos``)."""

from __future__ import annotations

from collections.abc import Sequence

from cerebro.models import Hit


class SentenceTransformerEncoder:
    """``normalize_embeddings=True`` para o Qdrant usar produto interno como cosseno."""

    dimension = 1024

    def __init__(self, model_name: str) -> None:
        self._model_name = model_name

    def encode(self, texts: Sequence[str]) -> list[list[float]]:
        raise NotImplementedError("Fase 2 — uv sync --extra modelos")


class CrossEncoderReranker:
    def __init__(self, model_name: str) -> None:
        self._model_name = model_name

    def rerank(self, question: str, hits: Sequence[Hit], top: int) -> list[Hit]:
        raise NotImplementedError("Fase 3")
