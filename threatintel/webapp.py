from __future__ import annotations

import argparse
from html import escape
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .config import load_config
from .monitor import MonitorService
from .storage import Storage

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000


def build_service(config_path: str | None, db_path: str | None) -> MonitorService:
    config = load_config(config_path)
    storage = Storage(Path(db_path or "threatintel.db"))
    storage.init()
    return MonitorService(config, storage)


def render_index(
    service: MonitorService,
    saved: str | None = None,
    alerts: str | None = None,
) -> str:
    findings = service.storage.list_findings(limit=20)
    watchlist_html = "".join(
        f'<span class="tag">{escape(keyword)}</span>' for keyword in service.config.watchlist
    )
    rows = []
    for finding in findings:
        rows.append(
            "<tr>"
            f"<td class=\"meta\">{escape(finding.observed_at)}</td>"
            f"<td>{escape(finding.source)}</td>"
            "<td>"
            f"<strong>{escape(finding.title)}</strong>"
            f"<div class=\"meta\">{escape(finding.snippet)}</div>"
            "</td>"
            f"<td>{finding.score}</td>"
            "</tr>"
        )
    table_body = "".join(rows) or (
        "<tr><td colspan=\"4\" class=\"meta\">No findings stored yet.</td></tr>"
    )
    banner = ""
    if saved is not None and alerts is not None:
        banner = (
            "<div class=\"card\">"
            f"<strong>Collection complete.</strong> Saved {escape(saved)} findings "
            f"and generated {escape(alerts)} alerts."
            "</div>"
        )
    return f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>Threat Intel Dashboard</title>
    <style>
      body {{
        font-family: \"Segoe UI\", system-ui, sans-serif;
        margin: 0;
        background: #f6f7fb;
        color: #1f2633;
      }}
      header {{
        background: #101828;
        color: #fff;
        padding: 24px 32px;
      }}
      main {{
        padding: 32px;
        max-width: 1100px;
        margin: 0 auto;
      }}
      .cards {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 16px;
      }}
      .card {{
        background: #fff;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 12px 24px rgba(16, 24, 40, 0.08);
        margin-bottom: 16px;
      }}
      .actions {{
        display: flex;
        gap: 12px;
        margin: 20px 0;
        flex-wrap: wrap;
      }}
      .btn {{
        background: #2563eb;
        color: #fff;
        padding: 10px 18px;
        border-radius: 8px;
        border: none;
        text-decoration: none;
        cursor: pointer;
        font-weight: 600;
      }}
      .btn.secondary {{
        background: #0f172a;
      }}
      table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 16px;
      }}
      th,
      td {{
        text-align: left;
        padding: 12px;
        border-bottom: 1px solid #e4e7ec;
      }}
      .meta {{
        color: #475467;
        font-size: 0.9rem;
      }}
      .tag {{
        display: inline-block;
        background: #e0f2fe;
        color: #0369a1;
        padding: 2px 8px;
        border-radius: 999px;
        font-size: 0.75rem;
        margin-right: 4px;
      }}
    </style>
  </head>
  <body>
    <header>
      <h1>Threat Intelligence Monitoring</h1>
      <p class=\"meta\">Simulated dark web monitoring dashboard</p>
    </header>
    <main>
      {banner}
      <div class=\"cards\">
        <div class=\"card\">
          <h3>Watchlist</h3>
          <p>{watchlist_html}</p>
        </div>
        <div class=\"card\">
          <h3>Alert threshold</h3>
          <p>{service.config.alert_threshold}</p>
        </div>
        <div class=\"card\">
          <h3>Database</h3>
          <p class=\"meta\">{escape(str(service.storage.path))}</p>
        </div>
      </div>
      <div class=\"actions\">
        <form action=\"/run\" method=\"post\">
          <button class=\"btn\" type=\"submit\">Run collection</button>
        </form>
        <a class=\"btn secondary\" href=\"/config\">View config</a>
      </div>
      <div class=\"card\">
        <h3>Recent findings</h3>
        <table>
          <thead>
            <tr>
              <th>Observed</th>
              <th>Source</th>
              <th>Title</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            {table_body}
          </tbody>
        </table>
      </div>
    </main>
  </body>
</html>"""


def render_config(service: MonitorService) -> str:
    watchlist_html = "".join(
        f'<span class="tag">{escape(keyword)}</span>' for keyword in service.config.watchlist
    )
    sources = "".join(
        f"<li>{escape(source.name)} ({escape(source.type)})</li>"
        for source in service.config.sources
    )
    return f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>Threat Intel Config</title>
    <style>
      body {{
        font-family: \"Segoe UI\", system-ui, sans-serif;
        margin: 0;
        background: #f6f7fb;
        color: #1f2633;
      }}
      header {{
        background: #101828;
        color: #fff;
        padding: 24px 32px;
      }}
      main {{
        padding: 32px;
        max-width: 900px;
        margin: 0 auto;
      }}
      .card {{
        background: #fff;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 12px 24px rgba(16, 24, 40, 0.08);
        margin-bottom: 16px;
      }}
      .tag {{
        display: inline-block;
        background: #e0f2fe;
        color: #0369a1;
        padding: 2px 8px;
        border-radius: 999px;
        font-size: 0.75rem;
        margin-right: 4px;
      }}
      a {{
        color: #2563eb;
        text-decoration: none;
      }}
    </style>
  </head>
  <body>
    <header>
      <h1>Configuration</h1>
      <p>Threat monitoring settings</p>
    </header>
    <main>
      <div class=\"card\">
        <h3>Watchlist</h3>
        <p>{watchlist_html}</p>
      </div>
      <div class=\"card\">
        <h3>Alert threshold</h3>
        <p>{service.config.alert_threshold}</p>
      </div>
      <div class=\"card\">
        <h3>Sources</h3>
        <ul>
          {sources}
        </ul>
      </div>
      <a href=\"/\">Back to dashboard</a>
    </main>
  </body>
</html>"""


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        service = build_service(self.server.config_path, self.server.db_path)
        if parsed.path == "/":
            body = render_index(
                service,
                saved=(query.get("saved") or [None])[0],
                alerts=(query.get("alerts") or [None])[0],
            )
            self._send_html(body)
            return
        if parsed.path == "/config":
            body = render_config(service)
            self._send_html(body)
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not Found")

    def do_POST(self) -> None:
        if self.path == "/run":
            service = build_service(self.server.config_path, self.server.db_path)
            saved, alerts = service.run_once()
            self.send_response(HTTPStatus.SEE_OTHER)
            self.send_header("Location", f"/?saved={saved}&alerts={alerts}")
            self.end_headers()
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not Found")

    def _send_html(self, body: str) -> None:
        encoded = body.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


class DashboardServer(HTTPServer):
    def __init__(self, server_address: tuple[str, int], config_path: str | None, db_path: str | None):
        self.config_path = config_path or os.getenv("THREATINTEL_CONFIG")
        self.db_path = db_path or os.getenv("THREATINTEL_DB", "threatintel.db")
        super().__init__(server_address, DashboardHandler)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Threat intelligence web dashboard")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Host interface")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to bind")
    parser.add_argument("--config", default=None, help="Path to config JSON")
    parser.add_argument("--db", default=None, help="Path to SQLite DB")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    server = DashboardServer((args.host, args.port), args.config, args.db)
    print(f"Serving dashboard on http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
