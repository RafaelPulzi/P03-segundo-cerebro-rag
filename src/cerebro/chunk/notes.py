"""Chunking de nota do vault (ADR 0001)."""

from __future__ import annotations

from cerebro.models import Chunk, Document

_SEPARADOR = " › "


def _estimar_tokens(texto: str) -> float:
    return len(texto.split()) * 1.3


def _secoes(document: Document) -> list[tuple[str, str]]:
    """Divide o texto em seções ``(trilha, corpo)``, uma por heading.

    A trilha começa no título do documento e é substituída pelo texto do ``#``
    quando a nota tem heading de nível 1. Heading dentro de bloco de código é ignorado.
    """
    trilha: dict[int, str] = {0: document.title}
    em_codigo = False
    secoes: list[tuple[str, list[str]]] = []
    corpo_atual: list[str] = []
    secoes.append((document.title, corpo_atual))
    for linha in document.text.splitlines():
        if linha.lstrip().startswith("```"):
            em_codigo = not em_codigo
        if not em_codigo and linha.startswith("#"):
            nivel = len(linha) - len(linha.lstrip("#"))
            texto_heading = linha[nivel:].strip()
            if 1 <= nivel <= 6 and texto_heading:
                trilha = {n: t for n, t in trilha.items() if 0 < n < nivel}
                if nivel > 1 and not trilha:
                    trilha[0] = document.title
                trilha[nivel] = texto_heading
                contexto = _SEPARADOR.join(trilha[n] for n in sorted(trilha))
                corpo_atual = []
                secoes.append((contexto, corpo_atual))
                continue
        corpo_atual.append(linha)
    return [(contexto, "\n".join(linhas).strip()) for contexto, linhas in secoes if "\n".join(linhas).strip()]


def _paragrafos(corpo: str) -> list[str]:
    """Separa por linha em branco, sem cortar bloco de código cercado no meio."""
    paragrafos: list[str] = []
    atual: list[str] = []
    em_codigo = False
    for linha in corpo.splitlines():
        if linha.lstrip().startswith("```"):
            em_codigo = not em_codigo
        if not linha.strip() and not em_codigo:
            if atual:
                paragrafos.append("\n".join(atual))
                atual = []
            continue
        atual.append(linha)
    if atual:
        paragrafos.append("\n".join(atual))
    return paragrafos


def _quebrar(corpo: str, max_tokens: int) -> list[str]:
    """Agrupa parágrafos em pedaços de até ``max_tokens``; um parágrafo nunca é cortado."""
    if _estimar_tokens(corpo) <= max_tokens:
        return [corpo]
    pedacos: list[str] = []
    atual: list[str] = []
    for paragrafo in _paragrafos(corpo):
        candidato = "\n\n".join([*atual, paragrafo])
        if atual and _estimar_tokens(candidato) > max_tokens:
            pedacos.append("\n\n".join(atual))
            atual = [paragrafo]
        else:
            atual = [*atual, paragrafo]
    if atual:
        pedacos.append("\n\n".join(atual))
    return pedacos


def split_note(document: Document, max_tokens: int) -> list[Chunk]:
    """Um chunk por heading (``#``, ``##``, ``###``).

    ``context`` é a trilha ``Título › H2 › H3``. Seção maior que ``max_tokens`` (estimado como
    palavras × 1,3) quebra por parágrafo mantendo o mesmo ``context``. Bloco de código não é
    cortado no meio.
    """
    chunks: list[Chunk] = []
    for contexto, corpo in _secoes(document):
        for pedaco in _quebrar(corpo, max_tokens):
            chunks.append(
                Chunk(
                    chunk_id=f"{document.source_id}::{len(chunks)}",
                    source_id=document.source_id,
                    text=pedaco,
                    context=contexto,
                    metadata=document.metadata,
                )
            )
    return chunks
