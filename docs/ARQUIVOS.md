# Mapa de arquivos — Segundo Cérebro RAG

Cada arquivo e pasta deste repositório, com o motivo de existir. Se você abriu um
arquivo e não sabe por que ele está aqui, a resposta tem que estar nesta página.

> [!important] Regra de manutenção
> Arquivo novo entra nesta tabela **no mesmo commit** em que é criado. Arquivo
> removido sai daqui no mesmo commit. Um mapa desatualizado é pior que nenhum,
> porque ensina errado.

## Árvore

```
P03-segundo-cerebro-rag/
├── config/
│   └── cerebro.example.toml
├── deploy/
│   └── docker-compose.yml
├── docs/
│   ├── agents/
│   │   ├── domain.md
│   │   ├── issue-tracker.md
│   │   └── triage-labels.md
│   ├── adr/
│   │   ├── 0001-chunk-por-heading-com-frontmatter.md
│   │   ├── 0002-tudo-local-ollama-e-bge-m3.md
│   │   └── 0003-recuperacao-hibrida-com-rrf.md
│   ├── ARQUITETURA.md
│   ├── ARQUIVOS.md
│   ├── LEVANTAMENTO.md
│   ├── PASSO-A-PASSO.md
│   └── SPEC-MVP-FASES-1-3.md
├── eval/
│   ├── resultados/
│   │   └── .gitkeep
│   ├── vault/            ← vault sintético de demonstração (corpus do eval)
│   ├── perguntas.yaml
│   └── run.py
├── src/
│   └── cerebro/
│       ├── adapters/
│       │   ├── __init__.py
│       │   ├── ollama.py
│       │   ├── qdrant_store.py
│       │   └── sentence_transformer.py
│       ├── chunk/
│       │   ├── __init__.py
│       │   └── notes.py
│       ├── ingest/
│       │   ├── __init__.py
│       │   ├── obsidian.py
│       │   ├── pdf.py
│       │   ├── web.py
│       │   └── youtube.py
│       ├── retrieve/
│       │   ├── __init__.py
│       │   ├── bm25.py
│       │   ├── fusion.py
│       │   └── hybrid.py
│       ├── __init__.py
│       ├── cli.py
│       ├── models.py
│       ├── ports.py
│       └── settings.py
├── tests/
│   ├── fixtures/
│   │   └── vault/
│   │       ├── 01 - Pessoal/
│   │       │   └── 01.1 - Diary/
│   │       │       └── 2026-10-16.md
│   │       └── 05 - PARA Method/
│   │           └── 05 - Projetos/
│   │               └── 03Hard/
│   │                   └── 🔵 P99 - Projeto de Teste.md
│   ├── support/
│   │   ├── __init__.py
│   │   └── fases.py
│   ├── unit/
│   │   ├── test_architecture.py
│   │   ├── test_chunking.py
│   │   ├── test_eval_set.py
│   │   ├── test_fusion.py
│   │   ├── test_models.py
│   │   └── test_obsidian_ingest.py
│   ├── __init__.py
│   └── conftest.py
├── .editorconfig
├── .gitattributes
├── .gitignore
├── CLAUDE.md
├── pyproject.toml
├── README.md
├── SPEC.md
└── uv.lock
```

## Arquivo por arquivo

### Raiz do repositório

| Arquivo | O que é e por que existe |
|---|---|
| `.editorconfig` | Padroniza encoding, fim de linha e indentação entre editores (VS Code, JetBrains, Vim) para o diff não sujar por espaço. |
| `.gitattributes` | Fim de linha LF no repositório. |
| `.gitignore` | O que nunca vai para o Git: ambiente, caches de modelo e de índice, configuração local com o caminho do vault. |
| `CLAUDE.md` | Instruções operacionais para o agente: ordem de leitura, fase atual, regra de avaliação antes de mudança e o que nunca fazer com o corpus. |
| `pyproject.toml` | Pacote, dependências (base leve e extras por fonte e por modelo), comando cerebro e configuração de ruff, mypy e pytest. |
| `README.md` | Porta de entrada: o que o RAG sobre o vault faz, como rodar, documentos e narrativas de valor. |
| `SPEC.md` | Especificação: escopo, requisitos por fonte e aplicação, métricas de qualidade de recuperação, cenários de aceite e questões em aberto. |
| `uv.lock` | Versões exatas de todas as dependências, inclusive dos extras; gerado por `uv lock`. |

### `config/`

Configuração local. Só o .example é versionado.

| Arquivo | O que é e por que existe |
|---|---|
| `cerebro.example.toml` | Modelo de configuração: caminho do vault, exclusões, modelos, endereços do Qdrant e do Ollama e parâmetros de recuperação. |

### `deploy/`

Serviços locais em Docker.

| Arquivo | O que é e por que existe |
|---|---|
| `docker-compose.yml` | Sobe Qdrant e Ollama com volumes persistentes (índice e modelos ficam fora do repositório). |

### `docs/`

| Arquivo | O que é e por que existe |
|---|---|
| `ARQUITETURA.md` | Arquitetura: pipeline de ponta a ponta, contratos Document/Chunk/Hit, estratégias de chunking por tipo, recuperação híbrida com RRF, avaliação e portas. |
| `ARQUIVOS.md` | Este mapa. Explica cada arquivo e pasta do repositório; todo arquivo novo entra aqui no mesmo commit. |
| `LEVANTAMENTO.md` | Inventário: hardware para os modelos, ferramentas, modelos a baixar, privacidade do corpus, conhecimento e custos. |
| `PASSO-A-PASSO.md` | Plano de execução em fases, com tarefas, comandos, critério de pronto e commits sugeridos. |
| `SPEC-MVP-FASES-1-3.md` | Spec de trabalho do MVP (fases 1–3) pronto para agente: user stories, decisões de implementação e de teste, sintetizado do SPEC, da arquitetura e dos testes @pendente. Publicado como a issue #1 (`ready-for-agent`); a issue é a cópia de trabalho, este arquivo é o espelho local. |

### `docs/agents/`

Configuração dos skills de engenharia (mattpocock-skills): onde ficam as issues, os labels de triagem e como consumir a documentação de domínio.

| Arquivo | O que é e por que existe |
|---|---|
| `domain.md` | Regras de consumo da documentação de domínio: ler GLOSSARY.md (quando existir) e os ADRs da área antes de explorar; usar o vocabulário do glossário; apontar conflito com ADR. |
| `issue-tracker.md` | Onde as issues vivem (GitHub Issues via gh CLI) e as convenções de criar, ler, rotular e fechar. |
| `triage-labels.md` | Mapeamento dos cinco papéis canônicos de triagem para os labels do tracker (iguais aos nomes dos papéis). |

### `docs/adr/`

| Arquivo | O que é e por que existe |
|---|---|
| `0001-chunk-por-heading-com-frontmatter.md` | ADR 0001 — por que a nota é dividida por heading e o frontmatter vira metadado filtrável, em vez de janelas fixas de tokens. |
| `0002-tudo-local-ollama-e-bge-m3.md` | ADR 0002 — por que geração e embedding rodam localmente (Ollama e bge-m3) e nenhuma API externa é usada. |
| `0003-recuperacao-hibrida-com-rrf.md` | ADR 0003 — BM25 e busca densa fundidos por Reciprocal Rank Fusion, com o conjunto de avaliação como critério de toda mudança. |

### `eval/`

Avaliação da recuperação: o conjunto de perguntas com resposta esperada e o script que mede.

| Arquivo | O que é e por que existe |
|---|---|
| `perguntas.yaml` | Conjunto de avaliação público: 12 perguntas sobre o vault sintético de demonstração (`eval/vault/`), cada uma com as notas que deveriam ser recuperadas. As 10 perguntas reais (Q5) vivem fora do repositório. |
| `run.py` | Mede recall@5 e MRR@10 de cada configuração de recuperação sobre perguntas.yaml e grava o resultado datado (RF-07). Fase 3. |

### `eval/vault/`

Vault sintético de demonstração: corpus público que `cerebro ingest` e `cerebro eval` usam na demo e no CI. Mesma estrutura PARA e frontmatter do vault real; todo conteúdo é inventado — nenhuma nota pessoal (fronteira público/privado do SPEC). Projetos sintéticos P90–P98 em `05 - Projetos/{02Medium,03Hard,04Extreme}/` (estufa, encurtador, hábitos, k8s caseiro, compilador, finanças, xadrez, scanner, receitas) e uma área (`06 - Áreas/🔵 Treino de Corrida.md`), cada um alvo de ao menos uma pergunta do `perguntas.yaml`.

### `eval/resultados/`

Resultados datados de cada execução da avaliação (JSON ignorado pelo Git; só a tabela vai para o README).

| Arquivo | O que é e por que existe |
|---|---|
| `.gitkeep` | Mantém a pasta de resultados no repositório, já que os JSON são ignorados. |

### `src/cerebro/`

O pacote. Núcleo puro (models, chunk, retrieve.fusion) no centro; ingest, embed, store e generate fazem I/O.

| Arquivo | O que é e por que existe |
|---|---|
| `__init__.py` | Marca o pacote. |
| `cli.py` | Linha de comando: ingest, ask, eval, summarize e serve. Só traduz argumentos; a lógica está nos módulos. |
| `models.py` | Contratos do pipeline: Document (o que a ingestão produz), Chunk (o que é indexado) e Hit (o que a recuperação devolve). |
| `ports.py` | Interfaces dos componentes com I/O — Encoder, VectorStore, Reranker, Generator — para trocar modelo ou banco sem tocar no pipeline. |
| `settings.py` | Configuração tipada lida de config/cerebro.toml e de variáveis CEREBRO_*. |

### `src/cerebro/adapters/`

Implementações das portas: modelo de embedding, Qdrant, reranker e Ollama.

| Arquivo | O que é e por que existe |
|---|---|
| `__init__.py` | Marca o subpacote de adaptadores. |
| `ollama.py` | Generator sobre a API HTTP do Ollama em localhost, com o prompt que obriga a citar as fontes [n]. Fase 2. |
| `qdrant_store.py` | VectorStore sobre Qdrant: coleção com o frontmatter como payload indexado para filtro. Fase 2. |
| `sentence_transformer.py` | Encoder e Reranker com sentence-transformers (bge-m3 e bge-reranker-v2-m3), carregados só quando usados. Fase 2. |

### `src/cerebro/chunk/`

Estratégias de divisão por tipo de documento. Puras: recebem Document, devolvem Chunk.

| Arquivo | O que é e por que existe |
|---|---|
| `__init__.py` | Marca o subpacote de chunking. |
| `notes.py` | Chunking de nota por heading, com a trilha de headings como contexto e o frontmatter herdado como metadado (RF-02, ADR 0001). Fase 1. |

### `src/cerebro/ingest/`

Uma fonte por arquivo; cada uma devolve Document. Ninguém fora daqui sabe de onde veio o texto.

| Arquivo | O que é e por que existe |
|---|---|
| `__init__.py` | Marca o subpacote de ingestão. |
| `obsidian.py` | Fonte do vault: varre os .md respeitando exclusões, lê frontmatter e calcula o hash de conteúdo para a ingestão incremental (RF-01, RF-03). Fase 1. |
| `pdf.py` | Fonte de PDF com texto por página, tabela como Markdown e OCR para página escaneada (RF-08). Fase 4. |
| `web.py` | Fonte de página web: baixa e limpa com trafilatura (absorve o Web Scraper). Fase 4+. |
| `youtube.py` | Fonte de vídeo do YouTube: transcrição com carimbo de tempo (RF-09). Fase 5. |

### `src/cerebro/retrieve/`

Recuperação: BM25, densa, fusão RRF e reranking.

| Arquivo | O que é e por que existe |
|---|---|
| `__init__.py` | Marca o subpacote de recuperação. |
| `bm25.py` | Índice lexical BM25 com tokenização para português e filtro por metadado. Fase 3. |
| `fusion.py` | Reciprocal Rank Fusion: combina listas ranqueadas pela posição, sem calibrar escalas de score (RF-06, ADR 0003). Fase 3. |
| `hybrid.py` | Orquestra a recuperação: filtro, BM25 e denso em paralelo, RRF e reranker; abaixo do limiar responde que não encontrou (RNF-06). Fases 2–3. |

### `tests/`

Testes como especificação. Fases futuras marcadas com @pendente.

| Arquivo | O que é e por que existe |
|---|---|
| `__init__.py` | Torna tests um pacote, para importar tests.support. |
| `conftest.py` | Fixtures compartilhadas: caminho do vault sintético. |

### `tests/fixtures/vault/01 - Pessoal/01.1 - Diary/`

| Arquivo | O que é e por que existe |
|---|---|
| `2026-10-16.md` | Nota de diário sintética que precisa ser ignorada pela exclusão padrão. |

### `tests/fixtures/vault/05 - PARA Method/05 - Projetos/03Hard/`

| Arquivo | O que é e por que existe |
|---|---|
| `🔵 P99 - Projeto de Teste.md` | Nota sintética com frontmatter e três headings, usada nos cenários C1 e C4. |

### `tests/support/`

Apoio aos testes.

| Arquivo | O que é e por que existe |
|---|---|
| `__init__.py` | Marca o pacote de apoio. |
| `fases.py` | Marcador @pendente(fase, o_que) para testes escritos antes da implementação. |

### `tests/unit/`

Testes sem serviço externo.

| Arquivo | O que é e por que existe |
|---|---|
| `test_architecture.py` | O núcleo puro (models, ports, chunk, retrieve.fusion) não importa I/O nem modelos (RNF-05). Roda desde a Fase 0. |
| `test_chunking.py` | Especificação do chunking por heading com contexto e metadado herdado (RF-02, cenário C1). Fase 1. |
| `test_eval_set.py` | O conjunto de avaliação é válido: toda pergunta tem ao menos uma nota esperada e nenhuma pergunta se repete. Roda desde a Fase 0. |
| `test_fusion.py` | Especificação da fusão RRF: posição, não score; ausência numa lista; desempate estável (RF-06). Fase 3. |
| `test_models.py` | Contratos do pipeline: imutabilidade e texto de embedding com o contexto prefixado. Roda desde a Fase 0. |
| `test_obsidian_ingest.py` | Especificação da ingestão do vault: frontmatter, exclusão do diário, título sem emoji e detecção de mudança (RF-01, RF-03). Fase 1. |

### Outras pastas

Pastas que agrupam subpastas ou que ainda não existem no disco (marcadas como *prevista* na árvore — nascem na fase do PASSO-A-PASSO indicada).

| Pasta | Para que serve |
|---|---|
| `tests/fixtures/vault/` | Vault sintético mínimo para os testes, com a mesma estrutura de pastas e frontmatter do real — nenhum conteúdo pessoal. |
