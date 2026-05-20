#!/usr/bin/env python3
"""Fetch YouTube oEmbed JSON.

Usage:
  python scripts/fetch_youtube_oembed.py --video-id KZEPlZKGq7A --out artifacts/video6/oembed.json

Notes:
- Prints HTTP status code.
- If status is 200, writes JSON to --out and prints sha256.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.parse
import urllib.request


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--video-id', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--url-kind', choices=['youtu.be', 'watch', 'embed'], default='youtu.be')
    args = ap.parse_args()

    vid = args.video_id
    if args.url_kind == 'youtu.be':
        video_url = f'https://youtu.be/{vid}'
    elif args.url_kind == 'watch':
        video_url = f'https://www.youtube.com/watch?v={vid}'
    else:
        video_url = f'https://www.youtube.com/embed/{vid}'

    oembed_url = 'https://www.youtube.com/oembed?url=' + urllib.parse.quote(video_url, safe='') + '&format=json'

    req = urllib.request.Request(
        oembed_url,
        headers={
            # Keep it simple: YouTube oEmbed should respond without special headers.
            'User-Agent': 'pages-mixed-state-youtube oembed fetcher',
        },
        method='GET',
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read()
            status = getattr(resp, 'status', 200)
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read() if hasattr(e, 'read') else b''
    except Exception as e:
        print(f'ERROR: {e}', file=sys.stderr)
        return 2

    print(f'HTTP {status}')

    if status != 200:
        # Print a short body preview for debugging.
        preview = body[:200].decode('utf-8', errors='replace').replace('\n', '\\n')
        if preview:
            print(f'Body preview: {preview}')
        return 1

    # Validate JSON.
    try:
        obj = json.loads(body.decode('utf-8'))
    except Exception as e:
        print(f'ERROR: response was 200 but not JSON: {e}', file=sys.stderr)
        return 3

    out_path = args.out
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write('\n')

    h = sha256_bytes(body)
    print(f'Wrote: {out_path}')
    print(f'sha256(body): {h}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
