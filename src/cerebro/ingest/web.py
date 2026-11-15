"""Fonte: página web."""

from __future__ import annotations

from cerebro.models import Document


def read_page(url: str) -> Document:
    """Conteúdo principal sem menu nem rodapé; ``metadata["url"]`` e ``metadata["fetched_at"]``."""
    raise NotImplementedError("Fase 4 — uv sync --extra web")
