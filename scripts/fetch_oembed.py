#!/usr/bin/env python3
"""DEPRECATED: use scripts/fetch_youtube_oembed_json.py instead.

Fetch YouTube oEmbed JSON for a given video URL.

Example:
  python scripts/fetch_oembed.py --url 'https://youtu.be/VIDEOID' --out artifacts/video6/oembed.json

Behavior:
- Prints the HTTP status code.
- Writes --out only on HTTP 200.
- On non-200, prints a short body preview to aid debugging.

Notes:
- oEmbed fields can change over time; storing the raw JSON response is still a
  useful, lightweight publication proof.
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


def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _write_atomic_json(path: str | Path, obj: object) -> None:
    """Write JSON with newline atomically, creating parent dirs if needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = None
    try:
        tmp = tempfile.NamedTemporaryFile(
            "w", delete=False, dir=str(path.parent), encoding="utf-8", newline=""
        )
        json.dump(obj, tmp, ensure_ascii=False, indent=2, sort_keys=True)
        tmp.write("\n")
        tmp.close()
        os.replace(tmp.name, path)
    except Exception:
        if tmp is not None:
            try:
                os.unlink(tmp.name)
            except OSError:
                pass
        raise


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="YouTube watch URL or youtu.be short URL")
    ap.add_argument("--out", required=True, help="Path to write JSON to (only on HTTP 200)")
    args = ap.parse_args(argv)

    base = "https://www.youtube.com/oembed"
    qs = urllib.parse.urlencode({"url": args.url, "format": "json"})
    req = urllib.request.Request(
        f"{base}?{qs}",
        headers={
            "User-Agent": "pages-mixed-state-youtube oembed fetcher",
            "Accept-Encoding": "identity",
        },
    )

    status: int | None = None
    body: bytes = b""

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
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    print(f"HTTP {status}")

    if status != 200:
        preview = body[:200].decode("utf-8", errors="replace").replace("\n", "\\n")
        if preview:
            print(f"Body preview: {preview}")
        return 1

    try:
        obj = json.loads(body.decode("utf-8"))
    except Exception as e:
        print(f"ERROR: response was 200 but not JSON: {e}", file=sys.stderr)
        return 3

    try:
        _write_atomic_json(args.out, obj)
    except Exception as e:
        print(f"ERROR: failed to write {args.out}: {e}", file=sys.stderr)
        return 4

    print(f"Wrote: {args.out}")
    print(f"sha256(body): {_sha256_bytes(body)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
