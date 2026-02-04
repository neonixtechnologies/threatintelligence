from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import sqlite3
from typing import Iterable

from .sources import Finding


SCHEMA = """
CREATE TABLE IF NOT EXISTS findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    snippet TEXT NOT NULL,
    score REAL NOT NULL,
    observed_at TEXT NOT NULL
);
"""


class Storage:
    def __init__(self, path: Path) -> None:
        self.path = path

    def init(self) -> None:
        with sqlite3.connect(self.path) as conn:
            conn.executescript(SCHEMA)

    def save_findings(self, findings: Iterable[Finding]) -> int:
        rows = [asdict(finding) for finding in findings]
        if not rows:
            return 0
        with sqlite3.connect(self.path) as conn:
            conn.executemany(
                """
                INSERT INTO findings (source, title, snippet, score, observed_at)
                VALUES (:source, :title, :snippet, :score, :observed_at)
                """,
                rows,
            )
        return len(rows)

    def list_findings(self, limit: int = 50) -> list[Finding]:
        with sqlite3.connect(self.path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT source, title, snippet, score, observed_at
                FROM findings
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            )
            return [Finding(**dict(row)) for row in cursor.fetchall()]
