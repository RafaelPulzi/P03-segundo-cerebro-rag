# Spec de trabalho — MVP (Fases 1–3) · tag v1.0.0

> Gerado a partir de `SPEC.md`, `docs/ARQUITETURA.md`, `docs/PASSO-A-PASSO.md` e dos testes
> `@pendente` existentes. Cobre as fases 1 a 3; a fase 0 (fundação) é pré-requisito,
> não escopo deste spec.
>
> **Publicado:** issue [#1](https://github.com/RafaelPulzi/P03-segundo-cerebro-rag/issues/1),
> label `ready-for-agent`. A issue é a cópia de trabalho; este arquivo é o espelho local.

## Problem Statement

O dono do vault acumula anos de notas no Obsidian (estrutura PARA, frontmatter com
`difficulty`, `project_status` etc.) e não consegue reencontrar o que já escreveu:
a busca nativa é lexical e por nota inteira, não responde perguntas, não cita a seção
exata e não filtra por metadado. Ferramentas de RAG em nuvem estão descartadas porque
o vault contém material pessoal — nada pode sair da máquina (ADR 0002).

Hoje o repositório tem apenas o esqueleto: contratos (`Document`, `Chunk`, `Hit`,
`Answer`), portas (`Encoder`, `VectorStore`, `Reranker`, `Generator`), CLI que responde
"ainda não implementado" e testes `@pendente` das fases 1 e 3.

## Solution

Um pipeline RAG local de ponta a ponta sobre o vault:

- **Fase 1 — Vault como corpus:** `cerebro ingest` varre o vault, transforma cada `.md`
  em `Document` (frontmatter como metadado, exclusões respeitadas), divide por heading
  em `Chunk` com a trilha de headings como contexto, e reindexa incrementalmente por
  hash de conteúdo.
- **Fase 2 — Perguntar com citação:** `cerebro ask "<pergunta>"` recupera os chunks
  relevantes (denso, via bge-m3 + Qdrant), monta o prompt, gera a resposta no Ollama
  e lista as notas citadas com caminho, heading e link `obsidian://`. Filtro
  `--where chave=valor`. `cerebro serve` expõe o mesmo fluxo por HTTP.
- **Fase 3 — Recuperação híbrida medida:** BM25 + denso fundidos por RRF (k=60),
  reranker cross-encoder opcional, e `cerebro eval` medindo recall@5 e MRR@10 nas
  quatro configurações (`dense`, `bm25`, `hybrid`, `hybrid+rerank`), com comparação
  contra a última execução gravada.

Pronto quando recall@5 ≥ 0,80 e MRR@10 ≥ 0,60 no conjunto de avaliação real (Q5).

## User Stories

1. Como dono do vault, quero rodar `cerebro ingest` e ver quantas notas foram indexadas, para saber que o corpus está pronto para perguntas.
2. Como dono do vault, quero que cada `.md` vire um `Document` com caminho relativo, título, frontmatter e corpo, para que a origem de cada resposta seja rastreável até a nota.
3. Como dono do vault, quero que o título da nota perca o emoji de status (`🔵`, etc.) mas o emoji sobreviva como metadado `status_prefix`, para buscar limpo sem perder a informação.
4. Como dono do vault, quero que o diário e as pastas de `exclude_globs` nunca sejam indexados por padrão, para que material íntimo não entre no índice sem decisão explícita minha (Q1).
5. Como dono do vault, quero que cada seção de heading vire um chunk com a trilha de headings como contexto ("P99 › Arquitetura"), para que a citação aponte a seção exata e o embedding carregue o assunto da nota.
6. Como dono do vault, quero que todo chunk herde o frontmatter da nota como metadado, para poder filtrar perguntas por `difficulty`, `project_status` ou pasta PARA.
7. Como dono do vault, quero que seção maior que o limite de tokens seja quebrada por parágrafo mantendo o mesmo contexto, para que nenhum chunk estoure a janela do encoder.
8. Como dono do vault, quero que a estrutura PARA (Projetos/Áreas/Recursos/Arquivos) do caminho vire metadado filtrável do chunk, para perguntar só sobre projetos ativos, por exemplo.
9. Como dono do vault, quero reingestão incremental por hash de conteúdo, para que editar uma nota reprocesse só ela (cenário C4) e a ingestão diária seja instantânea.
10. Como dono do vault, quero que nota apagada do vault saia do índice na próxima ingestão, para não receber citações de notas que não existem mais.
11. Como dono do vault, quero ver no final do `ingest` o resumo de novas, alteradas e removidas, para confiar que a detecção de mudança funciona.
12. Como dono do vault, quero perguntar `cerebro ask "quais projetos usam Raspberry Pi?"` e receber resposta em linguagem natural com as notas citadas `[n]`, para reencontrar conhecimento sem lembrar em que nota está.
13. Como dono do vault, quero cada citação com caminho + heading e link `obsidian://`, para abrir a nota citada com um clique.
14. Como dono do vault, quero filtrar a pergunta com `--where difficulty=03Hard --where project_status=parado`, para restringir a resposta a um recorte do vault (cenário C2).
15. Como dono do vault, quero que uma pergunta sem resposta no vault ("qual a capital da Mongólia?") devolva "não encontrei no vault" em vez de uma invenção, para confiar nas respostas que vêm com citação (cenário C3, RNF-06).
16. Como dono do vault, quero que geração e embedding rodem 100% em localhost (Ollama + bge-m3), para que nenhum conteúdo pessoal saia da máquina (ADR 0002, RNF-01).
17. Como dono do vault numa máquina de 15 GB RAM / 4 GB VRAM, quero o modelo 4B como padrão com o 8B documentado como opção, para que o pipeline caiba no hardware medido (Q2).
18. Como integrador, quero `cerebro serve` com `POST /ask`, `POST /search` e `GET /health`, para plugar outras ferramentas locais no mesmo pipeline (RF-13).
19. Como dono do vault, quero recuperação híbrida BM25 + denso fundida por RRF, para que termos exatos (siglas, códigos P99) e semântica funcionem juntos (RF-06).
20. Como dono do vault, quero um reranker cross-encoder opcional sobre o resultado fundido, para melhorar a precisão do topo quando a máquina aguenta.
21. Como mantenedor, quero `cerebro eval` medindo recall@5 e MRR@10 nas quatro configurações sobre `eval/perguntas.yaml`, para que toda mudança de chunking, embedding ou prompt seja julgada por número, não por impressão (ADR 0003).
22. Como mantenedor, quero que o `eval` compare com a última execução gravada e grave um resultado datado, para ver se uma mudança melhorou ou piorou.
23. Como mantenedor, quero a tabela comparando as quatro configurações no README (cenário C5), para que o portfólio mostre o híbrido superando o denso puro com números.
24. Como dono do vault, quero escrever minhas 10 perguntas reais na fase 3 e substituir o conjunto provisório (Q5), para que a métrica meça o meu uso de verdade.
25. Como visitante do repositório público, quero que código, testes e demo rodem contra o vault sintético de `tests/fixtures/`, para estudar o projeto sem que nenhum conteúdo pessoal seja exposto.
26. Como mantenedor, quero latência de ingestão (< 5 min para ~270 notas) e de resposta registradas em log e reportadas com honestidade na máquina real, para não prometer números que o hardware não entrega (Q2).

## Implementation Decisions

- **Contratos congelados.** `Document` (saída de toda ingestão), `Chunk` (saída de todo
  chunking, com `context` prefixado no `embedding_text`) e `Hit` já existem, são
  imutáveis (Pydantic frozen) e não mudam neste spec. Quem precisar de dado novo usa
  `metadata`.
- **Fronteira de fonte.** Só o módulo de ingestão Obsidian sabe que o texto veio de um
  vault; todo o resto do pipeline consome `Document`/`Chunk`. As fontes de PDF, web e
  YouTube ficam como stubs.
- **Núcleo puro.** Models, chunking e fusão RRF não fazem I/O nem importam modelos —
  o teste de arquitetura já garante e continua garantindo (RNF-05).
- **Portas e adaptadores.** `Encoder`, `VectorStore`, `Reranker` e `Generator` são
  Protocols já definidos. Implementações: sentence-transformers (bge-m3 e
  bge-reranker-v2-m3, carregados sob demanda), Qdrant (frontmatter como payload
  indexado para filtro `must`) e Ollama via HTTP em localhost. Modelo gerador padrão
  **4B** (decisão Q2); 8B vira opção de configuração documentada. A imagem Docker do
  Ollama fixada precisa subir de versão para suportar qwen3.
- **Ingestão incremental.** Estado = mapa `source_id → content_hash` persistido em
  cache local fora do controle de versão. A função de difere (`changed_sources`) é
  pura: recebe estado atual e anterior, devolve novos/alterados/removidos. O CLI
  orquestra: reindexa novos+alterados, chama `delete_sources` para removidos,
  regrava o estado.
- **Chunking de nota.** Um chunk por heading (`#`–`###`); trilha de headings separada
  por `›` como `context`; frontmatter herdado em `metadata`; seção acima de
  `max_tokens` quebra por parágrafo mantendo o mesmo `context` (ADR 0001).
- **Recuperação.** Orquestrador híbrido: filtro de metadado → BM25 top-50 + denso
  top-50 → RRF com k=60 (posição, nunca escala de score) → reranker nos 30 primeiros,
  corte em 8 → abaixo do limiar do reranker, `Answer(found=False)` com texto "não
  encontrei no vault". Na fase 2 roda só o denso; BM25/RRF/rerank entram na fase 3
  sem mudar a interface do orquestrador.
- **BM25 em disco**, com tokenização para português e o mesmo filtro de metadado do
  Qdrant, para que as duas pernas vejam o mesmo recorte.
- **Prompt de geração** obriga citação `[n]` referenciando os hits na ordem; a resposta
  final resolve `[n]` para caminho + heading + link `obsidian://`.
- **API HTTP** (FastAPI) é casca fina sobre o mesmo fluxo do `ask`: `POST /ask`,
  `POST /search` (só recuperação, sem geração), `GET /health`.
- **Avaliação.** Cada entrada do conjunto tem pergunta + notas esperadas. O runner
  mede recall@5 e MRR@10 por configuração, grava JSON datado (ignorado pelo Git) e
  imprime o delta contra a execução anterior. Regra de processo: nenhuma mudança de
  chunking/embedding/recuperação/prompt sem `eval` antes e depois no commit.
- **Fronteira público/privado.** O conjunto provisório que aponta para caminhos reais
  do vault é trocado por perguntas sobre o vault sintético antes do primeiro push;
  as 10 perguntas reais (Q5) vivem fora do repositório e só o agregado entra no README.

## Testing Decisions

- **Testes de comportamento externo, nunca de implementação:** o teste afirma o que a
  função devolve para uma entrada (chunks com contexto "P99 › Arquitetura"; conjuntos
  novos/alterados/removidos; score RRF ≈ 1/61 + 1/62), nunca como ela anda pela árvore
  ou tokeniza por dentro.
- **Seams já fixadas — nenhuma nova:** as funções puras `iter_vault_documents`,
  `changed_sources`, `split_note` e `reciprocal_rank_fusion`, exercitadas pelos testes
  `@pendente(1)` e `@pendente(3)` existentes, que viram verdes conforme as fases
  avançam. O orquestrador híbrido e o fluxo do `ask` são testados pelas portas, com os
  dublês da tabela da arquitetura (encoder determinístico por hash, store em memória
  com cosseno, reranker identidade, generator que devolve o prompt).
- **Fixture sintético como corpus de teste** (prior art: vault em `tests/fixtures/`
  com diário a excluir e nota P99 com frontmatter e três headings). Nada do vault real
  entra em teste.
- **Prior art:** `test_obsidian_ingest`, `test_chunking` e `test_fusion` são a
  especificação executável das fases 1 e 3; testes novos das fases 2–3 seguem o mesmo
  padrão (`@pendente(N, ...)` quando escritos antes da implementação, fixture
  sintético, dublês nas portas). O teste de arquitetura e o de formato do eval já
  rodam e precisam continuar verdes em todas as fases.
- **Qualidade medida, não testada por unidade:** recall@5 ≥ 0,80 e MRR@10 ≥ 0,60 são
  critério de pronto da fase 3 via `cerebro eval`, não assert de pytest.

## Out of Scope

- Fases 4–8: PDF/OCR, YouTube/`summarize`, grafo de wikilinks, resume-optimizer,
  busca multimodal por imagem. Ficam como roteiro de uma linha no README.
- Plugin Obsidian ou qualquer interface além de CLI + API (Q4).
- Indexação do diário (Q1 — excluído por padrão; ligar é escolha local invisível no
  repositório).
- Indexação das notas absorvidas/arquivadas do histórico PARA (Q3).
- Qualquer chamada de API externa de LLM ou embedding (ADR 0002).
- Calibração de escala entre scores BM25 e denso (RRF usa posição por decisão).

## Further Notes

- A fase 0 (git init, `uv sync`, docker compose, `ollama pull`, config local) é
  pré-requisito manual do dono; este spec assume Qdrant e Ollama no ar.
- Ordem de entrega = ordem das fases; cada fase tem critério de pronto próprio no
  PASSO-A-PASSO e as caixas de lá devem ser marcadas ao concluir.
- Processo: modo plano antes de código; arquivo novo entra em `docs/ARQUIVOS.md` no
  mesmo commit; decisão nova vira ADR; pergunta nova de avaliação entra no conjunto
  com a nota esperada.
- As metas de latência serão medidas na máquina real e reportadas como estão —
  compromisso de honestidade da decisão Q2.
