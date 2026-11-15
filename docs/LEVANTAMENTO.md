# Levantamento — Segundo Cérebro RAG

## 1. Hardware

| Recurso | Mínimo | Confortável | Por quê |
|---|---|---|---|
| RAM | 16 GB | 32 GB | Modelo de geração 8B quantizado ocupa ~5 GB; bge-m3 ~2 GB |
| GPU | nenhuma | NVIDIA com 8 GB+ | Sem GPU funciona; com GPU o `ask` cai de ~15 s para ~2 s |
| Disco | 10 GB | 20 GB | Modelos + índice Qdrant |

## 2. Ferramentas

| Ferramenta | Instalação (Windows) | Para quê |
|---|---|---|
| Python 3.12 + uv | `winget install Python.Python.3.12 astral-sh.uv` | Projeto |
| Docker Desktop | `winget install Docker.DockerDesktop` | Qdrant e Ollama |
| Tesseract (Fase 4) | `winget install UB-Mannheim.TesseractOCR` + idioma `por` | OCR de PDF escaneado |
| ffmpeg (Fase 5, opcional) | `winget install Gyan.FFmpeg` | Áudio quando o vídeo não tem legenda |

## 3. Modelos

| Modelo | Uso | Como obter | Tamanho |
|---|---|---|---|
| `BAAI/bge-m3` | Embedding multilíngue (o vault é em português) | baixado pelo sentence-transformers no primeiro uso | ~2,3 GB |
| `BAAI/bge-reranker-v2-m3` | Reranking por cross-encoder (Fase 3) | idem | ~2,3 GB |
| `qwen3:8b` (ou 4b, Q2) | Geração da resposta | `docker exec ollama ollama pull qwen3:8b` | ~5 GB |

## 4. Corpus e privacidade

- Vault local (caminho em `config/cerebro.toml`, fora do repositório) — lido, nunca escrito.
- `exclude_globs` padrão: `.obsidian/**`, `.trash/**`, `01 - Pessoal/01.1 - Diary/**` (questão Q1).
- O índice contém trechos do vault: o volume `qdrant-data` e `.cache/` são dado pessoal. Não sincronizar com nuvem.

## 5. Conhecimento por fase

| Fase | Assunto | Onde |
|---|---|---|
| 1 | Frontmatter YAML, wikilinks, estrutura de nota Obsidian | help.obsidian.md |
| 2 | Qdrant: coleções, payload, filtros | qdrant.tech/documentation |
| 3 | BM25, RRF (Cormack et al., 2009), cross-encoder, recall@k e MRR | sbert.net · *Introduction to Information Retrieval* (Manning) |
| 4 | Extração de PDF e OCR | pymupdf.readthedocs.io |
| 6 | Grafos de conhecimento simples | networkx.org |

## 6. Custos

R$ 0 — tudo local. Eletricidade de inferência em CPU.

## 7. Dependências com outros produtos

| Produto | Relação |
|---|---|
| Linter do vault (produto irmão) | Lê o mesmo vault; pode compartilhar o parser de frontmatter |
| Otimizador de currículo (produto futuro) | Usa `retrieve/` deste projeto (RF-11) |
| Plugin Obsidian (congelado) | Possível interface de pergunta dentro do Obsidian (Q4) |
| Lab de redes neurais (estudo irmão) | Capítulo de embeddings/atenção ajuda a explicar o que o bge-m3 faz |

## 8. Checklist de partida

- [ ] Q1 e Q2 respondidas
- [ ] Docker com Qdrant e Ollama de pé; `qwen3:8b` baixado
- [ ] `config/cerebro.toml` apontando para o vault
