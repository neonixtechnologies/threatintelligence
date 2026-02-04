# Threat Intelligence Dark Web Monitor

A lightweight Python application for simulating dark web monitoring workflows. It is designed to help security teams prototype collection, enrichment, and alerting pipelines without accessing real dark web sources.

## Features
- Configurable watchlists (keywords, priority tags, and routing).
- Pluggable source interface with a mock onion source for safe testing.
- SQLite-backed storage for findings and alerts.
- CLI for initializing storage, running a collection pass, and exporting results.

## Quick start
```bash
python -m threatintel.cli --init-db
python -m threatintel.cli --run-once
python -m threatintel.cli --list-findings
```

## Configuration
Update `config.json` or pass your own file via `--config`.

## Disclaimer
This project only simulates dark web monitoring. It does not connect to Tor or access live marketplaces.
