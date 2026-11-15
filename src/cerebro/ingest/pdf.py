"""Fonte: PDF."""

from __future__ import annotations

from pathlib import Path

from cerebro.models import Document


def read_pdf(path: Path) -> list[Document]:
    """Um ``Document`` por página; ``metadata["page"]`` é a citação. Página sem texto passa por OCR."""
    raise NotImplementedError("Fase 4 — uv sync --extra pdf")
