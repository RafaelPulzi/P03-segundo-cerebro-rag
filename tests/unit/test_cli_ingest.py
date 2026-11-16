"""O comando ``cerebro ingest`` imprime o resumo de novas/alteradas/removidas. Fase 1."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from cerebro.cli import app

runner = CliRunner()


def _env(tmp_path: Path) -> dict[str, str]:
    vault = tmp_path / "vault"
    vault.mkdir(exist_ok=True)
    (vault / "a.md").write_text("# A\n\ncorpo", encoding="utf-8")
    return {"CEREBRO_VAULT_PATH": str(vault), "CEREBRO_CACHE_DIR": str(tmp_path / ".cache")}


def test_ingest_prints_summary_counts(tmp_path: Path) -> None:
    result = runner.invoke(app, ["ingest"], env=_env(tmp_path))
    assert result.exit_code == 0
    assert "1 nova" in result.output
    assert "0 alterada" in result.output
    assert "0 removida" in result.output


def test_second_ingest_reports_zero_changes(tmp_path: Path) -> None:
    env = _env(tmp_path)
    runner.invoke(app, ["ingest"], env=env)
    result = runner.invoke(app, ["ingest"], env=env)
    assert result.exit_code == 0
    assert "0 nova" in result.output
