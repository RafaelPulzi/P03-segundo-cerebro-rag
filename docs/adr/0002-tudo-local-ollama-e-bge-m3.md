# ADR 0002 — Tudo local: Ollama e bge-m3

- **Estado:** aceita · **Data:** 2026-10-16

## Contexto

O corpus inclui notas pessoais. Mandar trechos para uma API externa é um risco de privacidade e um custo recorrente.

## Decisão

Geração por Ollama em `localhost:11434`; embedding por `BAAI/bge-m3` via sentence-transformers (multilíngue, bom em português, 8k de contexto). Os modelos ficam atrás das portas `Generator` e `Encoder`, então trocar de modelo é configuração.

## Consequências

- Custo zero e nenhum dado sai da máquina.
- Latência maior em CPU (RNF-03 aceita até 15 s).
- `sentence-transformers` traz PyTorch (~2 GB): fica no extra `modelos`, fora da instalação mínima dos testes.
