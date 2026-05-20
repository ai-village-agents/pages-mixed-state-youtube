#!/usr/bin/env python3
"""Fetch YouTube oEmbed JSON for a given video URL.

Example:
  python scripts/fetch_oembed.py --url 'https://youtu.be/VIDEOID' --out artifacts/video6/oembed.json

Notes:
- This is intended as a lightweight publication proof artifact.
- oEmbed fields can change over time; store the raw JSON response.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request


def fetch_oembed(video_url: str) -> dict:
    base = "https://www.youtube.com/oembed"
    qs = urllib.parse.urlencode({"url": video_url, "format": "json"})
    req = urllib.request.Request(f"{base}?{qs}", headers={"User-Agent": "ai-village-agent"})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read()
    try:
        return json.loads(body.decode("utf-8"))
    except Exception:
        # Preserve the raw body for debugging.
        raise RuntimeError(f"Failed to parse JSON from oEmbed. Raw body: {body[:2000]!r}")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="YouTube watch URL or youtu.be short URL")
    ap.add_argument("--out", required=True, help="Path to write JSON to")
    args = ap.parse_args(argv)

    data = fetch_oembed(args.url)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")

    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
