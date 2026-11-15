# Segundo Cérebro RAG

> Pipeline de ingestão, chunking, recuperação híbrida e geração cujo corpus é o meu próprio vault PARA — tudo local, com Ollama, sem nenhuma nota saindo da máquina.

## O problema

Nove ideias de IA no vault descreviam o mesmo pipeline — ingestão → embedding → recuperação → geração — mudando só a fonte (PDF, vídeo, página web, imagem) e o prompt final. O que tira isto da categoria "mais um RAG de tutorial" é o corpus: ~270 notas com estrutura PARA e frontmatter rico (`difficulty`, `project_status`, `tags`, `merge_code`). Isso permite perguntas que busca por texto não responde: *"quais projetos meus usam Raspberry Pi e estão parados?"* — com link para cada nota.

## Status

Fases em [`docs/PASSO-A-PASSO.md`](docs/PASSO-A-PASSO.md). **Fase atual: 0.**

## Como rodar

**Pré-requisitos:** Python 3.12, uv, Docker Desktop (Qdrant e Ollama), ~6 GB livres para modelos. Lista completa em [`docs/LEVANTAMENTO.md`](docs/LEVANTAMENTO.md).

```powershell
git clone https://github.com/RafaelPulzi/segundo-cerebro-rag.git
cd segundo-cerebro-rag
uv sync --extra modelos
copy config\cerebro.example.toml config\cerebro.toml     # caminho do vault, exclusões
docker compose -f deploy/docker-compose.yml up -d        # Qdrant :6333 · Ollama :11434
docker exec ollama ollama pull qwen3:8b
uv run cerebro ingest                                     # Fase 1
uv run cerebro ask "quais projetos usam Raspberry Pi?"    # Fase 2
uv run cerebro eval                                       # Fase 3: recall@5 e MRR do conjunto de avaliação
```

## Testes

```powershell
uv run pytest            # unidade + arquitetura; integração com Qdrant real via -m integration
uv run cerebro eval      # a métrica que decide se uma mudança de chunking ou modelo melhorou ou piorou
```

## Demonstração

<!-- Fase 2: GIF de `cerebro ask` respondendo com as notas citadas -->

## Stack

- **Python 3.12** · **pydantic v2** · **typer** + **rich** · **FastAPI**
- **Qdrant** (vetores + filtro por payload) · **rank-bm25** (lexical) · fusão RRF
- **sentence-transformers** com **BAAI/bge-m3** (embedding multilíngue) e cross-encoder para reranking
- **Ollama** (geração local) · **PyMuPDF** · **youtube-transcript-api** · **trafilatura**
- **pytest** · **ruff** · **mypy** · **Docker Compose**

## Documentação

| Documento | Para que serve |
|---|---|
| [`SPEC.md`](SPEC.md) | Requisitos, métricas de qualidade, cenários e questões abertas |
| [`docs/LEVANTAMENTO.md`](docs/LEVANTAMENTO.md) | Hardware, modelos, ferramentas, privacidade do corpus |
| [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md) | Pipeline, contratos de dados, estratégia de chunking e de recuperação |
| [`docs/PASSO-A-PASSO.md`](docs/PASSO-A-PASSO.md) | Fases com comandos e critério de pronto |
| [`docs/ARQUIVOS.md`](docs/ARQUIVOS.md) | Cada arquivo e por que existe |
| [`docs/adr/`](docs/adr/) | Decisões |

## Git e segurança

- O vault **nunca** entra no repositório: o caminho fica em `config/cerebro.toml` (ignorado). Índices do Qdrant e caches de modelo ficam em volumes Docker e `.cache/`.
- O conjunto de avaliação usa caminhos de nota, não conteúdo.
- Commits: `feat(chunk): divide nota por heading preservando frontmatter`, `perf(retrieve): RRF entre BM25 e denso melhora recall@5 de 0,62 para 0,81`, `test(eval): pergunta sobre projetos parados`.

## Histórias de uso

### Narrativa pessoal

Meu vault tinha 270 notas e uns 130 projetos que eu já não conseguia encontrar — a busca por texto não ajudava porque eu não lembrava das palavras exatas. Construí um pipeline de RAG sobre ele com modelo local: pergunto "quais projetos meus usam Raspberry Pi" e recebo a resposta com link para cada nota. O que fez diferença não foi o modelo: foi quebrar a nota por heading preservando o frontmatter, o que permite filtrar por dificuldade e status antes de buscar por semelhança, e ter um conjunto de perguntas com resposta certa para saber se cada mudança melhorou ou piorou.

### Uso em larga escala

É a arquitetura de qualquer base de conhecimento interna — onboarding, suporte de primeiro nível, due diligence jurídica. A parte difícil nunca é o LLM: é chunking por tipo de documento, recuperação híbrida com filtro por metadado e um conjunto de avaliação que detecte regressão quando alguém troca o modelo de embedding. Rodar local é também o desenho que passa por um comitê de privacidade.

## Origem

Produto P3 do roadmap pessoal de projetos — consolida 9 notas de ideias anteriores do vault.
