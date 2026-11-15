# SPEC — Segundo Cérebro RAG

| Campo | Valor |
|---|---|
| Código no vault | P3 · `03Hard` |
| Versão | 1.0 — 2026-10-16 |
| MVP | Fases 0 a 3 (vault, pergunta com citação, recuperação híbrida medida) |

## 1. Objetivo

Responder perguntas sobre o meu vault (e, depois, sobre PDFs, vídeos e páginas que eu ingerir) com citação da nota de origem, rodando inteiramente na minha máquina.

## 2. Requisitos funcionais

| ID | Requisito | Fase |
|---|---|---|
| RF-01 | Ingerir o vault: cada `.md` vira `Document` com caminho relativo, título, frontmatter e corpo; respeita `exclude_globs`. | 1 |
| RF-02 | Chunking de nota por heading (`#`, `##`, `###`), cada chunk herdando o frontmatter da nota como metadado e o caminho de headings como contexto. Chunk maior que o limite é quebrado por parágrafo. | 1 |
| RF-03 | Reingestão incremental: só reprocessa nota cujo hash de conteúdo mudou; nota apagada sai do índice. | 1 |
| RF-04 | `cerebro ask "<pergunta>"` devolve resposta e a lista de notas citadas (caminho + heading), com link `obsidian://`. | 2 |
| RF-05 | Filtro por metadado na pergunta: `--where difficulty=03Hard --where project_status=parado`. | 2 |
| RF-06 | Recuperação híbrida: BM25 + denso, fundidos por Reciprocal Rank Fusion (k=60), opcionalmente reranqueados por cross-encoder. | 3 |
| RF-07 | `cerebro eval` calcula recall@5 e MRR@10 sobre `eval/perguntas.yaml` e compara com a última execução gravada. | 3 |
| RF-08 | PDF: texto por página; tabela extraída como Markdown; página escaneada passa por OCR. | 4 |
| RF-09 | YouTube: transcrição em janelas de ~2 min com carimbo de tempo; `cerebro summarize <url>`. | 5 |
| RF-10 | Grafo de citações: wikilinks `[[...]]` entre notas e referências entre PDFs viram arestas; consulta "o que cita X". | 6 |
| RF-11 | `resume-optimizer`: compara currículo com vaga sobre o mesmo pipeline (amadurece em produto próprio futuro). | 7 |
| RF-12 | Imagem: embedding multimodal para busca por imagem. | 8 |
| RF-13 | API HTTP (`cerebro serve`): `POST /ask`, `POST /search`, `GET /health`. | 2 |

## 3. Requisitos não funcionais

| ID | Requisito | Verificação |
|---|---|---|
| RNF-01 | Nenhuma chamada de rede para fora de `localhost`. | Teste que falha se `httpx` tentar host externo; revisão |
| RNF-02 | Ingestão inicial do vault (~270 notas) em menos de 5 min em CPU. | Log de duração |
| RNF-03 | `ask` responde em menos de 15 s com modelo de 8B em CPU. | Log de duração |
| RNF-04 | Qualidade: recall@5 ≥ 0,80 e MRR@10 ≥ 0,60 no conjunto de avaliação ao fim da Fase 3. | `cerebro eval` |
| RNF-05 | Núcleo (`models`, `chunk`, `retrieve.fusion`) sem I/O. | `tests/unit/test_architecture.py` |
| RNF-06 | Resposta sem nota recuperada acima do limiar diz "não encontrei no vault" em vez de inventar. | Cenário C3 |

## 4. Cenários de aceite

- **C1 (RF-02):** nota com frontmatter `difficulty: 03Hard` e três headings gera três chunks, cada um com `difficulty` no metadado e o caminho de headings no texto de contexto.
- **C2 (RF-04, RF-05):** "quais projetos usam Raspberry Pi?" com `--where project_status=ativo` lista o P90 do vault de demonstração com link para a nota.
- **C3 (RNF-06):** "qual a capital da Mongólia?" responde que não encontrou no vault.
- **C4 (RF-03):** editar uma nota e rodar `ingest` reprocessa só ela.
- **C5 (RF-06, RNF-04):** híbrido supera denso puro no conjunto de avaliação — a tabela entra no README.

## 5. Rastreabilidade

| Requisito | Teste |
|---|---|
| RF-01, RF-03 | `tests/unit/test_obsidian_ingest.py` |
| RF-02 | `tests/unit/test_chunking.py` |
| RF-06 | `tests/unit/test_fusion.py` |
| RF-07 | `tests/unit/test_eval_set.py` (formato, roda já) e `eval/run.py` |
| RNF-05 | `tests/unit/test_architecture.py` |

## 6. Decisões (grill de 2026-11-10 — substitui as questões em aberto)

1. **Q1 (diário) → continua excluído por padrão.** Indexá-lo é escolha local do dono, invisível no repositório (ver fronteira público/privado abaixo).
2. **Q2 (modelo) → 4B por padrão.** A máquina medida tem 15,4 GB de RAM e GTX 1650 com 4 GB de VRAM: o `qwen3:8b` não cabe na GPU e espreme a RAM junto de Qdrant + bge-m3. O 8B fica documentado como opção para máquina maior. O alvo de latência do `ask` será **medido e honesto** nesta máquina (não prometer "< 15 s" sem cumprir). O que importa para o portfólio são as métricas de recuperação (recall@5, MRR), que rodam leves. Conserto registrado: a imagem fixada `ollama/ollama:0.6.2` é antiga demais para qwen3 — atualizar.
3. **Q3 (notas absorvidas) → não indexar no MVP.** As ideias continuam vivas no vault PARA local; não há backup perdido a resgatar. Histórico morto inflaria o corpus e pioraria o recall. **Bônus:** a estrutura PARA (Projetos/Áreas/Recursos/Arquivos) vira **metadado do chunk**, filtrável no `ask --where`.
4. **Q4 (interface) → só CLI + API na v1.0.0.** O plugin Obsidian dependia de outro produto do roadmap, que está congelado.
5. **Q5 (10 perguntas reais) → lição de casa do dono na largada da fase 0**, quando o projeto chegar à frente da fila; elas substituem o `eval/perguntas.yaml` provisório. Escrevê-las hoje, meses antes, geraria perguntas erradas.

### Decisões de escopo da mesma sessão

- **MVP = fases 0–3** (ingestão incremental por hash, Qdrant + Ollama, híbrido BM25 + RRF, eval com 4 configurações), tag v1.0.0. **Fases 4–8 (PDF/OCR, YouTube, grafo, resume-optimizer, multimodal) viram roteiro futuro** de uma linha cada no README.
- **Fronteira público/privado dura:** o repositório público contém apenas o **vault sintético de demonstração** (o fixture); código, eval e demo rodam contra ele. O vault real é alvo local configurado fora do repo; números do eval real entram no README só como resultado agregado. **Nada com caminho, título ou conteúdo de nota pessoal é commitado** — o `eval/perguntas.yaml` atual, que aponta para caminhos reais do vault, será trocado antes do primeiro push.
- Repositório público no GitHub desde o início da retomada (ver LEVANTAMENTO-GERAL §11).
