#!/usr/bin/env python3
"""Fetch YouTube oEmbed JSON and write it to disk atomically."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DEFAULT_UA = "pages-mixed-state-youtube oembed fetch/1.0"


def write_atomic_json(path: Path, obj: object) -> None:
    """Write JSON (with newline) to a temp file then atomically replace."""
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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Fetch YouTube oEmbed JSON to a file.")
    ap.add_argument("--url", required=True, help="YouTube watch URL or youtu.be short URL")
    ap.add_argument("--out", required=True, help="Destination JSON path (written only on HTTP 200)")
    ap.add_argument("--user-agent", default=DEFAULT_UA, help="User-Agent header (default: %(default)s)")
    ap.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout in seconds (default: %(default)s)")
    args = ap.parse_args(argv)

    qs = urllib.parse.urlencode({"url": args.url, "format": "json"})
    req = urllib.request.Request(
        f"https://www.youtube.com/oembed?{qs}",
        headers={
            "User-Agent": args.user_agent,
            "Accept-Encoding": "identity",
        },
    )

    status: int | None = None
    body: bytes | None = None

    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as resp:
            status = getattr(resp, "status", 200)
            body = resp.read()
    except urllib.error.HTTPError as e:
        status = e.code
        try:
            body = e.read()
        except Exception:
            body = b""
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if status != 200:
        print(f"oEmbed HTTP {status}; not writing {args.out}")
        return 3

    try:
        obj = json.loads(body.decode("utf-8") if body is not None else "")
    except Exception as e:
        print(f"ERROR: JSON parse failed: {e}", file=sys.stderr)
        return 1

    try:
        write_atomic_json(Path(args.out), obj)
    except Exception as e:
        print(f"ERROR: failed to write {args.out}: {e}", file=sys.stderr)
        return 1

    print(f"wrote {args.out} (oEmbed HTTP 200)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
