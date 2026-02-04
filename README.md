# Threat Intelligence Dark Web Monitor

A lightweight Python application for simulating dark web monitoring workflows. It is designed to help security teams prototype collection, enrichment, and alerting pipelines without accessing real dark web sources.

## Features
- Configurable watchlists (keywords, priority tags, and routing).
- Pluggable source interface with a mock onion source for safe testing.
- SQLite-backed storage for findings and alerts.
- Web dashboard for running collection passes and reviewing findings.

## Quick start
Start the web dashboard:
```bash
python -m threatintel
```

Then open <http://127.0.0.1:5000> in your browser to run collections and review findings.

You can point at a custom config or database path:
```bash
python -m threatintel --config config.json --db threatintel.db --port 5000
```

### Environment variables
- `THREATINTEL_CONFIG`: override the default config path.
- `THREATINTEL_DB`: override the database location.

## Configuration
Update `config.json` or pass your own file via `--config`.

## Disclaimer
This project only simulates dark web monitoring. It does not connect to Tor or access live marketplaces.
