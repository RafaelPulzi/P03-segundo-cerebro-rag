"""Fonte: o vault Obsidian."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from pathlib import Path

from cerebro.models import Document


def iter_vault_documents(vault_path: Path, exclude_globs: Sequence[str]) -> Iterator[Document]:
    """Um ``Document`` por ``.md``, com ``source_id`` relativo ao vault (barra normal, também no Windows).

    Frontmatter vira ``metadata``; o título é o nome do arquivo sem extensão nem prefixo de emoji
    de status (🟢 🟡 🔵 （；´д｀）ゞ), que fica em ``metadata["status_prefix"]``.
    """
    raise NotImplementedError("Fase 1")


def changed_sources(current: dict[str, str], previous: dict[str, str]) -> tuple[set[str], set[str], set[str]]:
    """Compara ``source_id → hash`` e devolve (novas, alteradas, removidas)."""
    raise NotImplementedError("Fase 1")
