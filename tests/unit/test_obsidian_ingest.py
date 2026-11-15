"""Ingestão do vault (RF-01, RF-03)."""

from __future__ import annotations

from pathlib import Path

from cerebro.ingest.obsidian import changed_sources, iter_vault_documents
from tests.support.fases import pendente

DEFAULT_EXCLUDES = (".obsidian/**", ".trash/**", "01 - Pessoal/01.1 - Diary/**")


@pendente(1, "iter_vault_documents")
def test_reads_frontmatter_and_strips_status_emoji(vault_dir: Path) -> None:
    (note,) = list(iter_vault_documents(vault_dir, DEFAULT_EXCLUDES))
    assert note.title == "P99 - Projeto de Teste"
    assert note.metadata["status_prefix"] == "🔵"
    assert note.metadata["difficulty"] == "03Hard"
    assert note.source_id.startswith("05 - PARA Method/")


@pendente(1, "iter_vault_documents")
def test_diary_is_excluded_by_default(vault_dir: Path) -> None:
    sources = [document.source_id for document in iter_vault_documents(vault_dir, DEFAULT_EXCLUDES)]
    assert not any("Diary" in source for source in sources)


@pendente(1, "changed_sources")
def test_changed_sources_splits_new_changed_and_removed() -> None:
    new, changed, removed = changed_sources(
        current={"a": "1", "b": "2*", "d": "4"}, previous={"a": "1", "b": "2", "c": "3"}
    )
    assert (new, changed, removed) == ({"d"}, {"b"}, {"c"})
