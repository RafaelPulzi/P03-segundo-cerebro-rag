"""Ingestão incremental de ponta a ponta, sem serviço externo (RF-01, cenário C4)."""

from __future__ import annotations

from pathlib import Path

from cerebro.ingest.pipeline import ingest_vault
from cerebro.ingest.state import load_state, save_state
from cerebro.settings import Settings


def _settings(tmp_path: Path) -> Settings:
    vault = tmp_path / "vault"
    vault.mkdir(exist_ok=True)
    return Settings(vault_path=vault, cache_dir=tmp_path / ".cache")


def _write_note(settings: Settings, name: str, text: str) -> None:
    (settings.vault_path / name).write_text(text, encoding="utf-8")


def test_state_round_trip(tmp_path: Path) -> None:
    state_path = tmp_path / ".cache" / "estado.json"
    assert load_state(state_path) == {}
    save_state(state_path, {"nota.md": "abc123"})
    assert load_state(state_path) == {"nota.md": "abc123"}


def test_first_run_reports_every_note_as_new(tmp_path: Path) -> None:
    settings = _settings(tmp_path)
    _write_note(settings, "a.md", "# A\n\ncorpo")
    _write_note(settings, "b.md", "# B\n\ncorpo")
    summary = ingest_vault(settings)
    assert (summary.new, summary.changed, summary.removed) == ({"a.md", "b.md"}, set(), set())


def test_second_run_without_edits_reports_zero_changes(tmp_path: Path) -> None:
    settings = _settings(tmp_path)
    _write_note(settings, "a.md", "# A\n\ncorpo")
    ingest_vault(settings)
    summary = ingest_vault(settings)
    assert (summary.new, summary.changed, summary.removed) == (set(), set(), set())
    assert summary.chunks == 0


def test_edited_note_is_the_only_one_reprocessed(tmp_path: Path) -> None:
    settings = _settings(tmp_path)
    _write_note(settings, "a.md", "# A\n\ncorpo")
    _write_note(settings, "b.md", "# B\n\ncorpo")
    ingest_vault(settings)
    _write_note(settings, "b.md", "# B\n\ncorpo editado")
    summary = ingest_vault(settings)
    assert (summary.new, summary.changed, summary.removed) == (set(), {"b.md"}, set())
    assert summary.chunks == 1


def test_removed_note_leaves_the_state(tmp_path: Path) -> None:
    settings = _settings(tmp_path)
    _write_note(settings, "a.md", "# A\n\ncorpo")
    _write_note(settings, "b.md", "# B\n\ncorpo")
    ingest_vault(settings)
    (settings.vault_path / "b.md").unlink()
    summary = ingest_vault(settings)
    assert summary.removed == {"b.md"}
    assert set(load_state(settings.cache_dir / "estado.json")) == {"a.md"}
