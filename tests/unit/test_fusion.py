"""Reciprocal Rank Fusion (RF-06)."""

from __future__ import annotations

import pytest

from cerebro.models import Chunk, Hit
from cerebro.retrieve.fusion import reciprocal_rank_fusion
from tests.support.fases import pendente


def _hit(chunk_id: str, score: float, retriever: str) -> Hit:
    chunk = Chunk(chunk_id=chunk_id, source_id=chunk_id, text=chunk_id, context="")
    return Hit(chunk=chunk, score=score, retriever=retriever)  # type: ignore[arg-type]


@pendente(3, "reciprocal_rank_fusion")
def test_item_ranked_well_in_both_lists_wins() -> None:
    bm25 = [_hit("a", 12.0, "bm25"), _hit("b", 9.0, "bm25"), _hit("c", 1.0, "bm25")]
    dense = [_hit("b", 0.91, "dense"), _hit("a", 0.90, "dense"), _hit("d", 0.20, "dense")]
    fused = reciprocal_rank_fusion([bm25, dense], k=60)
    assert [hit.chunk.chunk_id for hit in fused][:2] in (["a", "b"], ["b", "a"])
    assert fused[0].score == pytest.approx(1 / 61 + 1 / 62)
    assert all(hit.retriever == "fused" for hit in fused)


@pendente(3, "reciprocal_rank_fusion")
def test_scale_of_original_scores_is_ignored() -> None:
    huge = [_hit("x", 1e9, "bm25")]
    tiny = [_hit("y", 1e-9, "dense")]
    fused = reciprocal_rank_fusion([huge, tiny], k=60)
    assert fused[0].score == fused[1].score
    assert [hit.chunk.chunk_id for hit in fused] == ["x", "y"]
