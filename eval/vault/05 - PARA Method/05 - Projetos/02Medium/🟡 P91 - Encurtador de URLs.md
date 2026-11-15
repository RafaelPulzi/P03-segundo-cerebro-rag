---
type: product
project_status: planejado
difficulty: 02Medium
tags:
  - backend
  - filas
---

# P91 — Encurtador de URLs

Encurtador próprio para aprender backend sob carga.

## Arquitetura

API HTTP grava o link e publica o clique numa fila de eventos; um consumidor agrega as estatísticas por hora.

## Decisões

Redis para o contador quente, Postgres para o histórico.
