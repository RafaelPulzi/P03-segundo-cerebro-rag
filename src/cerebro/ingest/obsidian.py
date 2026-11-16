"""Fonte: o vault Obsidian."""

from __future__ import annotations

import fnmatch
import hashlib
import re
from collections.abc import Iterator, Sequence
from pathlib import Path

import frontmatter

from cerebro.models import Document, MetadataValue

_STATUS_PREFIX = re.compile(r"^(?P<prefix>[^\w\s]+)\s+(?P<title>.+)$")


def _coerce(value: object) -> MetadataValue:
    if isinstance(value, bool | int | float | str):
        return value
    if isinstance(value, list):
        return [str(item) for item in value]
    return str(value)


def _excluded(source_id: str, exclude_globs: Sequence[str]) -> bool:
    return any(fnmatch.fnmatch(source_id, glob) for glob in exclude_globs)


def iter_vault_documents(vault_path: Path, exclude_globs: Sequence[str]) -> Iterator[Document]:
    """Um ``Document`` por ``.md``, com ``source_id`` relativo ao vault (barra normal, também no Windows).

    Frontmatter vira ``metadata``; o título é o nome do arquivo sem extensão nem prefixo de emoji
    de status (🟢 🟡 🔵 …), que fica em ``metadata["status_prefix"]``. As pastas do caminho viram
    metadados filtráveis: ``para`` (pasta de topo, a categoria PARA) e ``folders`` (trilha completa).
    """
    for path in sorted(vault_path.rglob("*.md")):
        source_id = path.relative_to(vault_path).as_posix()
        if _excluded(source_id, exclude_globs):
            continue
        post = frontmatter.loads(path.read_text(encoding="utf-8"))
        metadata: dict[str, MetadataValue] = {key: _coerce(value) for key, value in post.metadata.items()}
        title = path.stem
        if match := _STATUS_PREFIX.match(title):
            metadata["status_prefix"] = match["prefix"]
            title = match["title"]
        if folders := source_id.split("/")[:-1]:
            metadata["para"] = folders[0]
            metadata["folders"] = folders
        yield Document(
            source_id=source_id,
            kind="note",
            title=title,
            text=post.content,
            metadata=metadata,
            content_hash=hashlib.sha256(post.content.encode("utf-8")).hexdigest(),
        )


def changed_sources(current: dict[str, str], previous: dict[str, str]) -> tuple[set[str], set[str], set[str]]:
    """Compara ``source_id → hash`` e devolve (novas, alteradas, removidas)."""
    new = set(current) - set(previous)
    removed = set(previous) - set(current)
    changed = {source_id for source_id in current.keys() & previous.keys() if current[source_id] != previous[source_id]}
    return new, changed, removed
