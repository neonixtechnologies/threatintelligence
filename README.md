# Threat Intelligence Dark Web Monitor

A lightweight Python application for simulating dark web monitoring workflows. It is designed to help security teams prototype collection, enrichment, and alerting pipelines without accessing real dark web sources.

## Features
- Configurable watchlists (keywords, priority tags, and routing).
- Pluggable source interface with a mock onion source for safe testing.
- SQLite-backed storage for findings and alerts.
- CLI for initializing storage, running a collection pass, and exporting results.

## Quick start
The CLI is exposed as a package entry point, so you can run the project with:
```bash
python -m threatintel --init-db
python -m threatintel --run-once
python -m threatintel --list-findings
```

You can also point at a custom config or database path:
```bash
python -m threatintel --config config.json --db threatintel.db --run-once
```

## Configuration
Update `config.json` or pass your own file via `--config`.

## Disclaimer
This project only simulates dark web monitoring. It does not connect to Tor or access live marketplaces.
