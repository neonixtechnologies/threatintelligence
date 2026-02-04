from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_config
from .monitor import MonitorService
from .storage import Storage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dark web monitoring simulation")
    parser.add_argument("--config", help="Path to config JSON", default=None)
    parser.add_argument("--db", help="Path to SQLite DB", default="threatintel.db")
    parser.add_argument("--init-db", action="store_true", help="Initialize database")
    parser.add_argument("--run-once", action="store_true", help="Run a single collection")
    parser.add_argument(
        "--list-findings",
        action="store_true",
        help="List recent findings",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Limit findings returned",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    config = load_config(args.config)
    storage = Storage(Path(args.db))

    if args.init_db:
        storage.init()
        print(f"Initialized database at {args.db}")

    if args.run_once:
        storage.init()
        service = MonitorService(config, storage)
        saved, alerts = service.run_once()
        print(f"Saved {saved} findings, generated {alerts} alerts")

    if args.list_findings:
        storage.init()
        findings = storage.list_findings(limit=args.limit)
        if not findings:
            print("No findings stored.")
        for finding in findings:
            print(
                f"[{finding.observed_at}] {finding.source} :: {finding.title} "
                f"(score={finding.score})"
            )
            print(f"  {finding.snippet}")


if __name__ == "__main__":
    main()
