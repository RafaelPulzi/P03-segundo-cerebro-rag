"""Fusão de rankings (ADR 0003)."""

from __future__ import annotations

from collections.abc import Sequence

from cerebro.models import Hit


def reciprocal_rank_fusion(rankings: Sequence[Sequence[Hit]], k: int = 60) -> list[Hit]:
    """``score(c) = Σ 1 / (k + posição_i(c))`` com posição a partir de 1; chunk ausente numa lista não pontua nela.

    Devolve ``Hit`` com ``retriever="fused"``, ordenado por score decrescente e, no empate, por ``chunk_id``.
    """
    raise NotImplementedError("Fase 3")
