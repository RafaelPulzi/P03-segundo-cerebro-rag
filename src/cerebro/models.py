"""Contratos de dados entre as etapas do pipeline."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

DocumentKind = Literal["note", "pdf", "transcript", "web", "image"]
MetadataValue = str | int | float | bool | list[str]


class _Frozen(BaseModel):
    model_config = ConfigDict(frozen=True)


class Document(_Frozen):
    source_id: str = Field(description="Caminho relativo no vault, URL ou hash do arquivo")
    kind: DocumentKind
    title: str
    text: str
    metadata: dict[str, MetadataValue] = {}
    content_hash: str


class Chunk(_Frozen):
    chunk_id: str
    source_id: str
    text: str
    context: str = Field(description="Trilha de headings ou página/minuto; prefixada no texto embutido")
    metadata: dict[str, MetadataValue] = {}

    @property
    def embedding_text(self) -> str:
        return f"{self.context}\n\n{self.text}" if self.context else self.text


class Hit(_Frozen):
    chunk: Chunk
    score: float
    retriever: Literal["bm25", "dense", "fused", "reranked"]


class Answer(_Frozen):
    question: str
    text: str
    citations: tuple[Hit, ...] = ()
    found: bool = True
