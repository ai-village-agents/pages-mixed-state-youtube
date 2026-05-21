#!/usr/bin/env python3
"""Check YouTube oEmbed HTTP status for one or more URLs."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
from pathlib import Path

import requests

DEFAULT_UA = "pages-mixed-state-youtube oembed fetch/1.0"
OEMBED_ENDPOINT = "https://www.youtube.com/oembed"


def read_urls(path: Path) -> list[str]:
    """Read URLs from a file, allowing blank lines and # comments."""
    urls: list[str] = []
    try:
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                urls.append(stripped)
    except FileNotFoundError:
        raise
    except OSError as e:
        raise RuntimeError(f"failed to read {path}: {e}") from e
    return urls


def iter_urls(args: argparse.Namespace) -> list[str]:
    if args.file:
        return read_urls(Path(args.file))
    urls = args.url or []
    return urls


def build_endpoint(url: str) -> str:
    qs = urllib.parse.urlencode({"url": url, "format": "json"})
    return f"{OEMBED_ENDPOINT}?{qs}"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Check YouTube oEmbed HTTP status.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--url", action="append", help="YouTube watch URL or youtu.be short URL (repeatable)")
    src.add_argument("--file", help="Path to file with one URL per line (# comments and blanks allowed)")
    ap.add_argument("--timeout", type=float, default=20.0, help="HTTP timeout in seconds (default: %(default)s)")
    ap.add_argument("--user-agent", default=DEFAULT_UA, help="User-Agent header (default: %(default)s)")
    ap.add_argument("--format", choices=["text", "json"], default="text", help="Output format (default: %(default)s)")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        urls = iter_urls(args)
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.file}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if not urls:
        print("ERROR: no URLs provided", file=sys.stderr)
        return 1

    headers = {"Accept-Encoding": "identity"}
    if args.user_agent:
        headers["User-Agent"] = args.user_agent

    session = requests.Session()
    results: list[dict[str, object]] = []

    for url in urls:
        endpoint = build_endpoint(url)
        try:
            resp = session.get(endpoint, headers=headers, timeout=args.timeout)
        except requests.RequestException as e:
            print(f"ERROR: request failed for {url}: {e}", file=sys.stderr)
            return 1
        status = resp.status_code
        reason = resp.reason or f"HTTP {status}"
        results.append({"url": url, "status": status, "reason": reason, "ok": status == 200})

    if args.format == "json":
        payload = [{"url": r["url"], "status": r["status"], "ok": r["ok"]} for r in results]
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        for r in results:
            line = f"{r['status']} {r['url']}"
            if not r["ok"]:
                line += f" (reason: {r['reason']})"
            print(line)

    has_non_200 = any(not r["ok"] for r in results)
    return 2 if has_non_200 else 0


if __name__ == "__main__":
    raise SystemExit(main())
