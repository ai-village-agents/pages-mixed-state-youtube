#!/usr/bin/env python3
"""Render a slides-only MP4 from an ffmpeg concat timing file.

This is mainly to make builds reproducible without committing machine-specific
absolute paths.

Example (Video 7):
  python scripts/render_slides_from_concat_timing.py \
    --timing-file slides/rendered_video7/concat_timing_video7.txt \
    --slides-dir slides/rendered_video7 \
    --out /tmp/video7_slides.mp4

Notes:
- The concat timing file should use basenames like `file 'slide_01.png'`.
- The script runs ffmpeg with `-nostdin` to avoid hangs in non-interactive runs.
"""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--timing-file', required=True)
    ap.add_argument('--slides-dir', required=True, help='Directory containing the slide images referenced by the timing file')
    ap.add_argument('--out', required=True)
    ap.add_argument('--fps', type=int, default=30)
    ap.add_argument('--pix-fmt', default='yuv420p')
    ap.add_argument('--vcodec', default='libx264')
    args = ap.parse_args()

    timing_file = Path(args.timing_file)
    slides_dir = Path(args.slides_dir)
    out = Path(args.out)

    if not timing_file.exists():
        print(f'ERROR: missing timing file: {timing_file}', file=sys.stderr)
        return 2
    if not slides_dir.exists():
        print(f'ERROR: missing slides dir: {slides_dir}', file=sys.stderr)
        return 2

    out.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        'ffmpeg',
        '-nostdin',
        '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(timing_file.name),
        '-r', str(args.fps),
        '-pix_fmt', args.pix_fmt,
        '-vcodec', args.vcodec,
        str(out),
    ]

    print('Running (from slides dir):')
    print('  (cd ' + shlex.quote(str(slides_dir)) + ' && ' + ' '.join(shlex.quote(c) for c in cmd) + ')')

    # Run from slides_dir so basenames resolve.
    proc = subprocess.run(cmd, cwd=str(slides_dir), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        print('ffmpeg failed (stderr tail):', file=sys.stderr)
        tail = proc.stderr[-2000:]
        print(tail, file=sys.stderr)
        return proc.returncode

    print(f'Wrote: {out}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
