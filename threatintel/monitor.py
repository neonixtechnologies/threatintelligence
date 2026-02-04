from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .config import AppConfig
from .sources import DarkWebSource, Finding, build_sources
from .storage import Storage


@dataclass(frozen=True)
class Alert:
    finding: Finding
    reason: str


def generate_alerts(findings: Iterable[Finding], threshold: float) -> list[Alert]:
    alerts: list[Alert] = []
    for finding in findings:
        if finding.score >= threshold:
            alerts.append(Alert(finding=finding, reason="Score above threshold"))
    return alerts


class MonitorService:
    def __init__(self, config: AppConfig, storage: Storage) -> None:
        self.config = config
        self.storage = storage
        self.sources: list[DarkWebSource] = build_sources(
            [source.__dict__ for source in config.sources]
        )

    def collect(self) -> tuple[list[Finding], list[Alert]]:
        findings: list[Finding] = []
        for source in self.sources:
            findings.extend(list(source.fetch(self.config.watchlist)))
        alerts = generate_alerts(findings, self.config.alert_threshold)
        return findings, alerts

    def run_once(self) -> tuple[int, int]:
        findings, alerts = self.collect()
        saved = self.storage.save_findings(findings)
        return saved, len(alerts)
