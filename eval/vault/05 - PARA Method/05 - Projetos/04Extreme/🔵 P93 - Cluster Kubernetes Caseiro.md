---
type: product
project_status: ativo
difficulty: 04Extreme
tags:
  - kubernetes
  - homelab
---

# P93 — Cluster Kubernetes Caseiro

Rodar Kubernetes em casa com três mini PCs usados.

## Arquitetura

k3s com um control plane e dois workers; armazenamento Longhorn replicado entre os nós.

## Lições

Atualização de nó drena os pods antes do reboot; sem isso o Longhorn degrada.
