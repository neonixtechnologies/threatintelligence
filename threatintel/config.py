from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class SourceConfig:
    name: str
    type: str
    seed: int | None = None


@dataclass(frozen=True)
class AppConfig:
    watchlist: list[str]
    alert_threshold: float
    sources: list[SourceConfig]

    @classmethod
    def load(cls, path: Path) -> "AppConfig":
        payload = json.loads(path.read_text())
        sources = [SourceConfig(**item) for item in payload.get("sources", [])]
        return cls(
            watchlist=list(payload.get("watchlist", [])),
            alert_threshold=float(payload.get("alert_threshold", 0.5)),
            sources=sources,
        )


DEFAULT_CONFIG_PATH = Path("config.json")


def load_config(path: str | None) -> AppConfig:
    target = Path(path) if path else DEFAULT_CONFIG_PATH
    return AppConfig.load(target)


def to_dict(config: AppConfig) -> dict[str, Any]:
    return {
        "watchlist": config.watchlist,
        "alert_threshold": config.alert_threshold,
        "sources": [source.__dict__ for source in config.sources],
    }
