# ADR 0001 — Chunk por heading com frontmatter como metadado

- **Estado:** aceita · **Data:** 2026-10-16

## Contexto

Janela fixa de N tokens corta uma seção no meio e mistura assuntos. As notas do vault já têm estrutura (headings) e metadado rico (frontmatter PARA).

## Decisão

Um chunk por heading; o texto embutido é prefixado pela trilha de headings (`P90 - Estufa Automatizada › Arquitetura`); o frontmatter inteiro vai para o payload do Qdrant e para o filtro do BM25. Seção maior que o limite quebra por parágrafo, mantendo o prefixo.

## Consequências

- Filtrar por `difficulty`, `project_status` ou `tags` antes da similaridade.
- Citação aponta para a seção, não só para a nota.
- Nota sem heading vira um chunk só — aceitável para notas curtas.
