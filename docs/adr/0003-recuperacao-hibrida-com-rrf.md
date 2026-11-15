# ADR 0003 — Recuperação híbrida com RRF e avaliação obrigatória

- **Estado:** aceita · **Data:** 2026-10-16

## Contexto

Busca densa erra nome próprio e sigla ("P90", "k3s", "Longhorn"); BM25 erra paráfrase. Somar scores exige calibrar escalas diferentes.

## Decisão

Rodar os dois e fundir pela posição, não pelo score: RRF com k = 60. Reranker opcional por cima. Toda mudança passa pelo `cerebro eval`, e o número vai no commit.

## Consequências

- Sem hiperparâmetro de peso entre lexical e denso.
- Ganho de qualidade é demonstrável com tabela, não com impressão.
