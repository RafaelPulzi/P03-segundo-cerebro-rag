"""Fonte: transcrição de vídeo do YouTube."""

from __future__ import annotations

from cerebro.models import Document


def read_transcript(video_url: str, languages: tuple[str, ...] = ("pt", "en")) -> Document:
    """Transcrição inteira; ``metadata["segments"]`` guarda os tempos para o chunking por janela."""
    raise NotImplementedError("Fase 5 — uv sync --extra youtube")
