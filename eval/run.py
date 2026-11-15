"""Avaliação da recuperação (RF-07, ADR 0003)."""

from __future__ import annotations

from collections.abc import Sequence


def recall_at_k(retrieved_sources: Sequence[str], expected_sources: Sequence[str], k: int) -> float:
    """Fração das fontes esperadas que aparecem entre as ``k`` primeiras recuperadas (sem repetir fonte)."""
    raise NotImplementedError("Fase 3")


def reciprocal_rank(retrieved_sources: Sequence[str], expected_sources: Sequence[str], k: int) -> float:
    """``1 / posição`` da primeira fonte esperada entre as ``k`` primeiras; 0 se nenhuma aparecer."""
    raise NotImplementedError("Fase 3")
