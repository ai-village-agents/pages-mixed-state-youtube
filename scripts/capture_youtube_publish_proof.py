#!/usr/bin/env python3
"""Capture proof artifacts that a YouTube video was published.

Creates a small, reproducible bundle:
- oembed.json (only on oEmbed HTTP 200)
- watch_headers.txt (status line + response headers)
- watch_body.html (only when --include-body is set)
- SHA256SUMS.txt (sha256 for every written file above)

Notes:
- Requests use Accept-Encoding: identity to avoid gzip artifacts (oEmbed and watch requests).
- Files are written atomically: temp file then rename.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Sequence

DEFAULT_UA = "pages-mixed-state-youtube publish proof/1.0"


def write_atomic_text(path: Path, content: str) -> None:
    """Write text to a temp file then atomically replace."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = None
    try:
        tmp = tempfile.NamedTemporaryFile("w", delete=False, dir=str(path.parent), encoding="utf-8", newline="")
        tmp.write(content)
        tmp.close()
        os.replace(tmp.name, path)
    except Exception:
        if tmp is not None:
            try:
                os.unlink(tmp.name)
            except OSError:
                pass
        raise


def write_atomic_bytes(path: Path, content: bytes) -> None:
    """Write bytes to a temp file then atomically replace."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = None
    try:
        tmp = tempfile.NamedTemporaryFile("wb", delete=False, dir=str(path.parent))
        tmp.write(content)
        tmp.close()
        os.replace(tmp.name, path)
    except Exception:
        if tmp is not None:
            try:
                os.unlink(tmp.name)
            except OSError:
                pass
        raise


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_sha256sums(out_dir: Path, files: Sequence[Path]) -> Path:
    """Write SHA256SUMS.txt in deterministic order for the given files."""
    sums_path = out_dir / "SHA256SUMS.txt"
    rel_paths = sorted((p.relative_to(out_dir) for p in files), key=lambda p: p.as_posix())
    lines = [
        f"{sha256_file(out_dir / rel)}  {rel.as_posix()}\n"
        for rel in rel_paths
    ]
    write_atomic_text(sums_path, "".join(lines))
    return sums_path


def _http_version(ver: int | None) -> str:
    if ver == 10:
        return "HTTP/1.0"
    if ver == 11:
        return "HTTP/1.1"
    if ver == 9:
        return "HTTP/0.9"
    return "HTTP/?"


def fetch_oembed(url: str, user_agent: str) -> tuple[int | None, dict | None, bytes | None]:
    base = "https://www.youtube.com/oembed"
    qs = urllib.parse.urlencode({"url": url, "format": "json"})
    req = urllib.request.Request(
        f"{base}?{qs}",
        headers={
            "User-Agent": user_agent,
            "Accept-Encoding": "identity",
        },
    )
    status: int | None = None
    body: bytes | None = None
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            status = getattr(r, "status", 200)
            body = r.read()
    except urllib.error.HTTPError as e:
        status = e.code
        try:
            body = e.read()
        except Exception:
            body = b""
    except Exception as e:
        print(f"ERROR: oEmbed fetch failed: {e}", file=sys.stderr)
        return None, None, None

    if status != 200 or body is None:
        return status, None, body

    try:
        obj = json.loads(body.decode("utf-8"))
    except Exception as e:
        print(f"ERROR: oEmbed 200 but JSON parse failed: {e}", file=sys.stderr)
        return status, None, body

    return status, obj, body


def fetch_watch(url: str, user_agent: str, want_body: bool) -> tuple[int | None, str | None, bytes | None]:
    headers = {
        "User-Agent": user_agent,
        "Accept-Encoding": "identity",
    }
    req = urllib.request.Request(url, headers=headers)
    status: int | None = None
    reason: str | None = None
    resp_headers: list[tuple[str, str]] = []
    body: bytes | None = None
    version: int | None = None

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            status = getattr(r, "status", 200)
            reason = getattr(r, "reason", None)
            version = getattr(r, "version", None)
            resp_headers = list(r.getheaders())
            if want_body:
                body = r.read()
    except urllib.error.HTTPError as e:
        status = e.code
        reason = e.reason
        version = getattr(e, "version", None)
        try:
            resp_headers = list(e.headers.items())
        except Exception:
            resp_headers = []
        try:
            if want_body:
                body = e.read()
        except Exception:
            body = b""
    except Exception as e:
        print(f"ERROR: watch fetch failed: {e}", file=sys.stderr)
        return None, None, None

    # Build headers text representation.
    status_line_parts = [_http_version(version), str(status if status is not None else "")]
    if reason:
        status_line_parts.append(str(reason))
    status_line = " ".join(part for part in status_line_parts if part)
    header_lines = [status_line] + [f"{k}: {v}" for k, v in resp_headers]
    headers_text = "\n".join(header_lines) + "\n"

    return status, headers_text, body


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Capture proof artifacts for a YouTube watch URL.")
    ap.add_argument("--url", required=True, help="YouTube watch URL or youtu.be short URL")
    ap.add_argument("--out-dir", required=True, help="Directory to write proof files into")
    ap.add_argument("--include-body", action="store_true", help="Also save watch_body.html")
    ap.add_argument("--user-agent", default=DEFAULT_UA, help="User-Agent header for requests (default: %(default)s)")
    args = ap.parse_args(argv)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ua = args.user_agent

    # 1) oEmbed (best effort)
    oembed_status, oembed_obj, _ = fetch_oembed(args.url, ua)
    written_files: list[Path] = []
    if oembed_status == 200 and oembed_obj is not None:
        oembed_path = out_dir / "oembed.json"
        write_atomic_text(oembed_path, json.dumps(oembed_obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        written_files.append(oembed_path)

    # 2) Watch page fetch
    watch_status, watch_headers_text, watch_body = fetch_watch(args.url, ua, args.include_body)
    if watch_headers_text is not None:
        watch_headers_path = out_dir / "watch_headers.txt"
        write_atomic_text(watch_headers_path, watch_headers_text)
        written_files.append(watch_headers_path)
    else:
        print("WARN: watch headers missing; skipping write", file=sys.stderr)

    if args.include_body and watch_body is not None:
        watch_body_path = out_dir / "watch_body.html"
        write_atomic_bytes(watch_body_path, watch_body)
        written_files.append(watch_body_path)

    # 3) SHA256 sums
    write_sha256sums(out_dir, written_files)

    # 4) Summary
    print(f"oEmbed HTTP {oembed_status if oembed_status is not None else 'error'}; watch HTTP {watch_status if watch_status is not None else 'error'}")

    # Non-zero on network/parse errors.
    if watch_headers_text is None:
        return 1
    if oembed_status == 200 and oembed_obj is None:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
