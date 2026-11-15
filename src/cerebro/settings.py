"""Configuração da aplicação."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, TomlConfigSettingsSource


class ModelSettings(BaseModel):
    embedding: str = "BAAI/bge-m3"
    reranker: str = "BAAI/bge-reranker-v2-m3"
    generator: str = "qwen3:8b"


class ServiceSettings(BaseModel):
    qdrant_url: str = "http://localhost:6333"
    ollama_url: str = "http://localhost:11434"
    collection: str = "vault"


class RetrievalSettings(BaseModel):
    candidates_per_retriever: int = 50
    rrf_k: int = 60
    rerank_top: int = 30
    final_top: int = 8
    max_chunk_tokens: int = 800


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CEREBRO_", env_nested_delimiter="__", toml_file="config/cerebro.toml", extra="ignore"
    )

    vault_path: Path
    exclude_globs: list[str] = [".obsidian/**", ".trash/**", "01 - Pessoal/01.1 - Diary/**"]
    models: ModelSettings = ModelSettings()
    services: ServiceSettings = ServiceSettings()
    retrieval: RetrievalSettings = RetrievalSettings()
    cache_dir: Path = Path(".cache")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (init_settings, env_settings, TomlConfigSettingsSource(settings_cls))
