#!/usr/bin/env python3
"""Poll YouTube oEmbed until the JSON is ready, delegating fetch to the writer."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Iterable

DEFAULT_UA = "pages-mixed-state-youtube oembed fetch/1.0"
FETCH_SCRIPT = Path(__file__).resolve().parent / "fetch_youtube_oembed_json.py"


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Poll YouTube oEmbed until it returns HTTP 200.")
    ap.add_argument(
        "--url",
        action="append",
        required=True,
        help="YouTube watch URL or youtu.be short URL (repeatable)",
    )
    ap.add_argument(
        "--out",
        required=True,
        help="Destination path (file for single URL; directory for multiple URLs)",
    )
    ap.add_argument(
        "--backend",
        choices=["curl", "python"],
        default="curl",
        help="HTTP backend for fetch (default: %(default)s)",
    )
    ap.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP timeout in seconds (default: %(default)s)",
    )
    ap.add_argument(
        "--connect-timeout",
        type=float,
        default=5.0,
        help="TCP connect timeout in seconds (default: %(default)s)",
    )
    ap.add_argument(
        "--interval",
        type=float,
        default=60.0,
        help="Seconds to wait between attempts when not ready (default: %(default)s)",
    )
    ap.add_argument(
        "--max-attempts",
        type=int,
        default=60,
        help="Maximum attempts before giving up (default: %(default)s)",
    )
    ap.add_argument(
        "--user-agent",
        default=DEFAULT_UA,
        help="User-Agent header (default: %(default)s)",
    )
    return ap.parse_args(argv)


def extract_video_id(url: str) -> str | None:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc.endswith("youtu.be"):
        slug = parsed.path.lstrip("/").split("/")[0]
        return slug or None
    if parsed.query:
        qs = urllib.parse.parse_qs(parsed.query)
        values = qs.get("v") or []
        if values and values[0]:
            return values[0]
    return None


def safe_slug(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]


def choose_slug(url: str, video_id: str | None) -> str:
    if video_id:
        cleaned = "".join(ch for ch in video_id if ch.isalnum() or ch in "-_")
        if cleaned:
            return cleaned
    return safe_slug(url)


def out_paths(urls: list[str], out_arg: str) -> dict[str, Path]:
    if not urls:
        raise ValueError("no URLs provided")
    out = Path(out_arg)
    if len(urls) == 1:
        return {urls[0]: out}

    if out.exists() and not out.is_dir():
        raise ValueError(f"--out must be a directory when multiple URLs are provided: {out}")
    out.mkdir(parents=True, exist_ok=True)
    mapping: dict[str, Path] = {}
    for url in urls:
        slug = choose_slug(url, extract_video_id(url))
        fname = f"oembed_{slug}.json"
        mapping[url] = out / fname
    return mapping


def run_fetch(url: str, dest: Path, args: argparse.Namespace) -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        str(FETCH_SCRIPT),
        "--url",
        url,
        "--out",
        str(dest),
        "--backend",
        args.backend,
        "--timeout",
        str(args.timeout),
        "--connect-timeout",
        str(args.connect_timeout),
    ]
    if args.user_agent:
        cmd.extend(["--user-agent", args.user_agent])
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def status_line(attempt: int, max_attempts: int, url: str, message: str) -> str:
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    return f"{ts} attempt {attempt}/{max_attempts} {url} - {message}"


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    urls = args.url or []
    try:
        targets = out_paths(urls, args.out)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    any_not_ready = False

    for url in urls:
        dest = targets[url]
        for attempt in range(1, args.max_attempts + 1):
            result = run_fetch(url, dest, args)
            rc = result.returncode
            stdout = (result.stdout or "").strip()
            stderr = (result.stderr or "").strip()

            if rc == 0:
                print(status_line(attempt, args.max_attempts, url, f"ready, wrote {dest}"))
                break

            if rc == 3:
                reason = "not ready (HTTP non-200)"
                last_line = stdout.splitlines()[-1].strip() if stdout else ""
                if last_line:
                    reason = f"not ready ({last_line})"
                print(status_line(attempt, args.max_attempts, url, reason))
                if attempt < args.max_attempts:
                    time.sleep(args.interval)
                    continue
                any_not_ready = True
                break

            message = f"error (exit {rc})"
            if stderr:
                message = f"{message}: {stderr}"
            elif stdout:
                message = f"{message}: {stdout}"
            print(status_line(attempt, args.max_attempts, url, message), file=sys.stderr)
            return 1

    if any_not_ready:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
