from __future__ import annotations

from dataclasses import dataclass
import random
import time
from typing import Iterable


@dataclass(frozen=True)
class Finding:
    source: str
    title: str
    snippet: str
    score: float
    observed_at: str


class DarkWebSource:
    name: str

    def fetch(self, watchlist: list[str]) -> Iterable[Finding]:
        raise NotImplementedError


class MockOnionSource(DarkWebSource):
    def __init__(self, name: str, seed: int | None = None) -> None:
        self.name = name
        self._rng = random.Random(seed)

    def fetch(self, watchlist: list[str]) -> Iterable[Finding]:
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        templates = [
            "{keyword} sale with exclusive access",
            "New dump listing {keyword}",
            "Forum chatter about {keyword} operations",
            "Private market advert: {keyword} tool",
        ]
        for keyword in watchlist:
            score = round(self._rng.uniform(0.3, 0.95), 2)
            title = self._rng.choice(templates).format(keyword=keyword)
            snippet = f"Mentioned keyword '{keyword}' in {self.name} discussions."
            yield Finding(
                source=self.name,
                title=title,
                snippet=snippet,
                score=score,
                observed_at=now,
            )


def build_sources(configs: list[dict[str, object]]) -> list[DarkWebSource]:
    sources: list[DarkWebSource] = []
    for config in configs:
        source_type = str(config.get("type", ""))
        if source_type == "mock":
            sources.append(
                MockOnionSource(
                    name=str(config.get("name", "mock-source")),
                    seed=config.get("seed") if isinstance(config.get("seed"), int) else None,
                )
            )
    return sources
