"""Linha de comando do Segundo Cérebro."""

from __future__ import annotations

from typing import Annotated

import typer

app = typer.Typer(no_args_is_help=True, add_completion=False, help="Perguntas ao vault, com citação, tudo local.")


def _pending(phase: int, what: str) -> typer.Exit:
    typer.secho(f"Ainda não implementado: {what} (Fase {phase} do PASSO-A-PASSO).", fg="yellow", err=True)
    return typer.Exit(code=2)


@app.command()
def ingest() -> None:
    """Indexa o vault de forma incremental: só notas novas, alteradas ou removidas."""
    raise _pending(1, "ingestão do vault")


@app.command()
def ask(
    question: str,
    where: Annotated[list[str] | None, typer.Option(help="Filtro de metadado chave=valor; repita para vários.")] = None,
) -> None:
    """Responde citando as notas usadas."""
    raise _pending(2, "pergunta com citação")


@app.command("eval")
def evaluate() -> None:
    """Mede recall@5 e MRR@10 sobre eval/perguntas.yaml para cada configuração de recuperação."""
    raise _pending(3, "avaliação")


@app.command()
def summarize(url: str) -> None:
    """Resume um vídeo do YouTube citando os minutos."""
    raise _pending(5, "resumo de vídeo")


@app.command()
def serve(port: int = 8000) -> None:
    """Sobe a API HTTP (POST /ask, POST /search, GET /health)."""
    raise _pending(2, "API HTTP")
