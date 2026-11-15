"""Formato do conjunto de avaliação."""

from __future__ import annotations

from pathlib import Path

import yaml

EVAL_FILE = Path(__file__).resolve().parents[2] / "eval" / "perguntas.yaml"


def test_every_question_has_expected_notes() -> None:
    questions = yaml.safe_load(EVAL_FILE.read_text(encoding="utf-8"))
    assert len(questions) >= 10
    for entry in questions:
        assert entry["pergunta"].strip()
        assert entry["esperadas"], entry["pergunta"]
        assert all(path.endswith(".md") for path in entry["esperadas"])


def test_questions_are_unique() -> None:
    questions = [entry["pergunta"] for entry in yaml.safe_load(EVAL_FILE.read_text(encoding="utf-8"))]
    assert len(questions) == len(set(questions))
