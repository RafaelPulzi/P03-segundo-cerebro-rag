# Contexto para o agente — Segundo Cérebro RAG

## Ordem de leitura

1. `SPEC.md` · 2. `docs/ARQUITETURA.md` · 3. `docs/PASSO-A-PASSO.md` — **fase atual: 2**.

## Regras de trabalho

- Modo plano antes de código.
- Testes da fase já existem com `@pendente(N, ...)`: `rg "pendente\(1" tests`.
- **Nenhuma mudança de chunking, embedding, recuperação ou prompt entra sem rodar `cerebro eval` antes e depois** e colar os dois números no commit.
- Cada fonte (`ingest/*`) devolve `Document`; cada estratégia de chunk devolve `Chunk`. Ninguém fora de `ingest/` sabe de onde veio o texto.
- `cerebro.core` (models, retrieve/fusion, chunk) não faz I/O — teste de arquitetura.
- Modelos e Qdrant são acessados por porta (`Encoder`, `VectorStore`, `Generator`); os testes de unidade usam dublês.

## Sempre documente tudo

- Arquivo novo → `docs/ARQUIVOS.md`. Decisão → ADR. Fase → caixas do PASSO-A-PASSO e linha acima.
- Pergunta nova no conjunto de avaliação → `eval/perguntas.yaml` com a nota esperada.

## Nunca

- Copiar conteúdo do vault para dentro do repositório (fixture é sintético, em `tests/fixtures/vault/`).
- Chamar API externa de LLM ou embedding: tudo local por desenho (ADR 0002).
- Indexar a pasta do diário sem a decisão da questão Q1 do SPEC.

## Comandos

```powershell
uv run pytest | uv run ruff check . | uv run mypy src
uv run cerebro ingest | ask "..." | eval | serve
```

## Agent skills

### Issue tracker

Issues live as GitHub Issues deste repositório, via `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Os cinco labels canônicos, sem renomear (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `GLOSSARY.md` na raiz (criado sob demanda) + `docs/adr/`. See `docs/agents/domain.md`.
