"""Regra de dependência (RNF-05)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE = Path(__file__).resolve().parents[2] / "src" / "cerebro"
PURE_MODULES = [
    PACKAGE / "models.py",
    PACKAGE / "ports.py",
    PACKAGE / "retrieve" / "fusion.py",
    *(PACKAGE / "chunk").glob("*.py"),
]
FORBIDDEN = (
    "httpx",
    "qdrant_client",
    "sentence_transformers",
    "fitz",
    "requests",
    "cerebro.adapters",
    "cerebro.ingest",
    "os",
)


def _imports(path: Path) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


@pytest.mark.parametrize("module_path", PURE_MODULES, ids=lambda path: path.relative_to(PACKAGE).as_posix())
def test_pure_modules_do_not_do_io(module_path: Path) -> None:
    offending = sorted(
        name for name in _imports(module_path) if any(name == f or name.startswith(f + ".") for f in FORBIDDEN)
    )
    assert offending == []
