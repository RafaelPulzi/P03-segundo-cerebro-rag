# Arquitetura — Segundo Cérebro RAG

## 1. Pipeline

```
  fontes                  normalização        chunking               indexação
┌──────────┐            ┌────────────┐     ┌──────────────┐     ┌──────────────────────┐
│ vault md │─ingest/──▶ │  Document  │──▶  │ chunk/       │──▶  │ Encoder (bge-m3)     │──▶ Qdrant (denso + payload)
│ pdf      │            │ (tipado)   │     │ por tipo     │     │ BM25 (tokens)        │──▶ índice BM25 em disco
│ youtube  │            └────────────┘     └──────────────┘     └──────────────────────┘
│ web      │
└──────────┘
                     pergunta ─▶ filtros PARA ─▶ BM25 top-50 ┐
                                              └▶ denso top-50 ┴▶ RRF ─▶ reranker top-8 ─▶ prompt ─▶ Ollama ─▶ resposta + citações
```

## 2. Contratos

```python
class Document:  # ingest/* devolve isto
    source_id: str  # caminho relativo no vault, URL ou hash do PDF
    kind: Literal["note", "pdf", "transcript", "web", "image"]
    title: str
    text: str
    metadata: dict[str, str | list[str]]  # frontmatter da nota, página do PDF, timestamp do vídeo
    content_hash: str


class Chunk:  # chunk/* devolve isto
    chunk_id: str  # source_id + posição
    source_id: str
    text: str  # o que vai para o encoder
    context: str  # "P90 - Estufa Automatizada › Arquitetura" — prefixado no embedding
    metadata: dict  # herdado do Document


class Hit:  # retrieve/* devolve isto
    chunk: Chunk
    score: float
    retriever: Literal["bm25", "dense", "fused", "reranked"]
```

## 3. Chunking por tipo

| Tipo | Estratégia | Por quê |
|---|---|---|
| Nota do vault | Um chunk por heading; frontmatter vira metadado; contexto = trilha de headings | A nota já é estruturada pelo autor; o heading é a unidade de sentido |
| PDF | Por página, juntando páginas curtas até ~800 tokens; tabela como Markdown | Página é a unidade de citação |
| Transcrição | Janelas de ~2 min com sobreposição de 15 s | Fala não tem parágrafo; tempo é a citação |
| Web | Por `<h2>`/`<h3>` após limpeza com trafilatura | Remove menu e rodapé antes de dividir |

## 4. Recuperação

1. **Filtro** por metadado (Qdrant `must` + filtro equivalente no BM25).
2. **BM25** e **denso** independentes, top-50 cada.
3. **RRF**: `score(d) = Σ 1 / (k + rank_i(d))`, k = 60. Sem calibrar escala entre os dois.
4. **Reranker** (cross-encoder) reordena os 30 primeiros e corta em 8.
5. Abaixo do limiar de score do reranker → "não encontrei no vault" (RNF-06).

## 5. Avaliação

`eval/perguntas.yaml`: pergunta + conjunto de notas esperadas. `cerebro eval` mede recall@5 e MRR@10 para cada configuração (`dense`, `bm25`, `hybrid`, `hybrid+rerank`) e grava em `eval/resultados/AAAA-MM-DD.json`. O README mostra a tabela da última execução.

## 6. Portas

| Porta | Implementação padrão | Dublê de teste |
|---|---|---|
| `Encoder` | `SentenceTransformerEncoder("BAAI/bge-m3")` | vetores determinísticos por hash |
| `VectorStore` | `QdrantStore` | dicionário em memória com cosseno |
| `Reranker` | `CrossEncoderReranker` | identidade |
| `Generator` | `OllamaGenerator("qwen3:8b")` | devolve o prompt |

## 7. Decisões

| ADR | Decisão |
|---|---|
| [0001](adr/0001-chunk-por-heading-com-frontmatter.md) | Nota dividida por heading com frontmatter como metadado |
| [0002](adr/0002-tudo-local-ollama-e-bge-m3.md) | Tudo local: Ollama para gerar, bge-m3 para embedding |
| [0003](adr/0003-recuperacao-hibrida-com-rrf.md) | Recuperação híbrida com RRF e avaliação obrigatória |
