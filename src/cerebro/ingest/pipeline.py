"""Ingestão incremental do vault: difere contra o estado anterior e regrava o índice."""

from __future__ import annotations

from dataclasses import dataclass

from cerebro.chunk.notes import split_note
from cerebro.ingest.obsidian import changed_sources, iter_vault_documents
from cerebro.ingest.state import load_state, save_state
from cerebro.settings import Settings

STATE_FILENAME = "estado.json"


@dataclass(frozen=True)
class IngestSummary:
    """Resultado de uma rodada: quais notas mudaram e quantos chunks foram reprocessados."""

    new: set[str]
    changed: set[str]
    removed: set[str]
    chunks: int


def ingest_vault(settings: Settings) -> IngestSummary:
    """Varre o vault, reprocessa só notas novas e alteradas e regrava ``.cache/estado.json``.

    Nota apagada sai do estado porque o estado regravado é sempre o vault atual inteiro.
    A indexação dos chunks (Qdrant/encoder) chega na Fase 2; aqui eles são só contados.
    """
    documents = list(iter_vault_documents(settings.vault_path, settings.exclude_globs))
    current = {document.source_id: document.content_hash for document in documents}
    state_path = settings.cache_dir / STATE_FILENAME
    new, changed, removed = changed_sources(current, load_state(state_path))
    to_process = new | changed
    chunks = sum(
        len(split_note(document, settings.retrieval.max_chunk_tokens))
        for document in documents
        if document.source_id in to_process
    )
    save_state(state_path, current)
    return IngestSummary(new=new, changed=changed, removed=removed, chunks=chunks)
