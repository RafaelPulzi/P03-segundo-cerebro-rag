"""Marcador de teste escrito antes da implementação."""

from __future__ import annotations

import pytest


def pendente(fase: int, o_que: str) -> pytest.MarkDecorator:
    return pytest.mark.skip(reason=f"Fase {fase} do PASSO-A-PASSO: {o_que}")
