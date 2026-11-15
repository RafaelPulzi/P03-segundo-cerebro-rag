"""Geração com Ollama local."""

from __future__ import annotations

from collections.abc import Sequence

from cerebro.models import Hit

PROMPT_TEMPLATE = """Você responde perguntas sobre o vault pessoal do usuário usando SOMENTE os trechos abaixo.
Cite cada afirmação com [n], onde n é o número do trecho. Se os trechos não respondem, diga
"não encontrei isso no vault" e nada mais.

{trechos}

Pergunta: {pergunta}
Resposta:"""


def build_prompt(question: str, hits: Sequence[Hit]) -> str:
    """Numera os trechos a partir de 1, cada um com ``context`` e ``source_id``."""
    raise NotImplementedError("Fase 2")


class OllamaGenerator:
    def __init__(self, base_url: str, model: str) -> None:
        self._base_url = base_url
        self._model = model

    def generate(self, prompt: str) -> str:
        raise NotImplementedError("Fase 2 — POST /api/generate com stream=false")
