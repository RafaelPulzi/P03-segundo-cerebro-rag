# Passo a passo — Segundo Cérebro RAG

Testes de fases futuras: `@pendente(N, ...)`. Ver o trabalho: `rg "pendente\(1" tests`.

## Fase 0 — Fundação

```powershell
cd D:\Projetos\P03-segundo-cerebro-rag
git init -b main
uv sync
uv run pytest            # modelos, avaliação e arquitetura passam; o resto skipped
docker compose -f deploy/docker-compose.yml up -d
copy config\cerebro.example.toml config\cerebro.toml
git add . ; git commit -m "chore: esqueleto do pipeline RAG com avaliação"
```

- [ ] Responder Q1 e Q2.
- [ ] Qdrant em http://localhost:6333/dashboard; `ollama pull` feito.

## Fase 1 — Vault como corpus

- [ ] `ingest/obsidian.py`: varre o vault, lê frontmatter, calcula hash, respeita exclusões (RF-01, RF-03).
- [ ] `chunk/notes.py`: por heading com contexto (RF-02, cenário C1).
- [ ] Índice de estado (`.cache/estado.json`: hash por nota) para a ingestão incremental.
- [ ] `cerebro ingest` mostrando quantas notas novas, alteradas e removidas.

**Pronto quando:** testes da Fase 1 verdes; ingestão real em menos de 5 min.

## Fase 2 — Perguntar com citação

```powershell
uv sync --extra modelos
```

- [ ] `embed/sentence_transformer.py`, `store/qdrant.py`.
- [ ] `generate/ollama.py` + `generate/prompts.py` com instrução de citar `[n]`.
- [ ] `cerebro ask` com `--where`; `cerebro serve` (FastAPI).
- [ ] Cenários C2 e C3 verificados à mão e gravados como pergunta no `eval/perguntas.yaml`.

## Fase 3 — Recuperação híbrida medida

- [ ] `retrieve/bm25.py`, `retrieve/fusion.py` (RRF), `retrieve/rerank.py`.
- [ ] `eval/run.py` com as quatro configurações; tabela no README (cenário C5).
- [ ] Responder Q5 e trocar o conjunto provisório pelas suas perguntas.

**Pronto quando:** recall@5 ≥ 0,80 e MRR@10 ≥ 0,60. **Tag:** `v1.0.0`.

## Fases 4 a 8

| Fase | Entrega | Pronto quando |
|---|---|---|
| 4 | `ingest/pdf.py` com tabela e OCR | PDF escaneado de teste responde pergunta sobre seu conteúdo |
| 5 | `ingest/youtube.py` + `cerebro summarize` | Resumo cita minutos do vídeo |
| 6 | `store/graph.py` com wikilinks | "o que cita P90?" lista as notas certas |
| 7 | `apps/resume.py` (base do otimizador de currículo) | Lacunas de um currículo de teste contra uma vaga de teste |
| 8 | Imagem com embedding multimodal | Busca por foto de um diagrama encontra a nota |
