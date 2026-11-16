"""Índice de estado da ingestão incremental: hash por nota, persistido em JSON."""

from __future__ import annotations

import json
from pathlib import Path


def load_state(path: Path) -> dict[str, str]:
    """Lê ``source_id → hash`` do disco; estado vazio quando o arquivo ainda não existe."""
    if not path.exists():
        return {}
    return {str(key): str(value) for key, value in json.loads(path.read_text(encoding="utf-8")).items()}


def save_state(path: Path, state: dict[str, str]) -> None:
    """Regrava o estado inteiro, criando a pasta de cache se preciso."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
