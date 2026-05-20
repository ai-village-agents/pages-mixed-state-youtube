#!/usr/bin/env python3
"""Capture reproducible proof artifacts for a built media file.

Creates:
- ffmpeg_i_<name>.txt: `ffmpeg -hide_banner -i <file>` stderr output.
- loudnorm_analysis_<name>.json: JSON printed by ffmpeg loudnorm filter (if audio present).
- SHA256SUMS.txt: sha256 of the input plus generated proof files.

Why:
- ffprobe isn't always available.
- These artifacts can be committed to document what was built without committing
  the heavy build outputs.

Example:
  python scripts/capture_media_proof.py \
    --input build/video7/video7_upload_candidate_draft_loud.mp4 \
    --out-dir artifacts/video7/proof_draft

Notes:
- Uses `-nostdin` to avoid hangs.
- Loudnorm analysis runs a full pass; it may take ~real-time.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def run_capture(cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout, proc.stderr


def extract_loudnorm_json(stderr: str) -> dict | None:
    # ffmpeg loudnorm prints JSON between braces on stderr; find the last {...} block.
    # This is intentionally conservative: we only accept something that parses as JSON.
    blocks = re.findall(r"\{[^\}]*\}", stderr, flags=re.DOTALL)
    for b in reversed(blocks):
        try:
            obj = json.loads(b)
            # Basic keys observed in loudnorm print_format=json.
            if isinstance(obj, dict) and ('input_i' in obj or 'output_i' in obj or 'target_offset' in obj):
                return obj
        except Exception:
            continue
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--out-dir', required=True)
    ap.add_argument('--i-target', default='-16')
    ap.add_argument('--tp-target', default='-1.5')
    ap.add_argument('--lra-target', default='11')
    args = ap.parse_args()

    inp = Path(args.input)
    out_dir = Path(args.out_dir)

    if not inp.exists():
        print(f'ERROR: missing input: {inp}', file=sys.stderr)
        return 2

    out_dir.mkdir(parents=True, exist_ok=True)

    stem = inp.name.replace(' ', '_')

    ffmpeg_i_path = out_dir / f'ffmpeg_i_{stem}.txt'
    loudnorm_path = out_dir / f'loudnorm_analysis_{stem}.json'
    sums_path = out_dir / 'SHA256SUMS.txt'

    # 1) ffmpeg -i capture
    cmd_i = ['ffmpeg', '-nostdin', '-hide_banner', '-i', str(inp)]
    rc, out, err = run_capture(cmd_i)
    # ffmpeg -i returns nonzero because no output specified; that's fine.
    ffmpeg_i_path.write_text(err, encoding='utf-8', errors='replace')
    print(f'Wrote: {ffmpeg_i_path}')

    # 2) loudnorm analysis pass (best effort)
    cmd_ln = [
        'ffmpeg', '-nostdin', '-hide_banner', '-y',
        '-i', str(inp),
        '-af', f"loudnorm=I={args.i_target}:TP={args.tp_target}:LRA={args.lra_target}:print_format=json",
        '-f', 'null', '-'
    ]
    rc2, out2, err2 = run_capture(cmd_ln)
    obj = extract_loudnorm_json(err2)
    if obj is None:
        # Store a short diagnostic instead of failing hard.
        loudnorm_path.write_text(
            json.dumps({
                'note': 'Could not parse loudnorm JSON from ffmpeg stderr. Is there an audio stream?',
                'ffmpeg_returncode': rc2,
                'stderr_tail': err2[-2000:],
            }, indent=2) + '\n',
            encoding='utf-8'
        )
        print(f'Wrote: {loudnorm_path} (diagnostic)')
    else:
        loudnorm_path.write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        print(f'Wrote: {loudnorm_path}')

    # 3) sha256 sums
    entries = [inp, ffmpeg_i_path, loudnorm_path]
    with sums_path.open('w', encoding='utf-8') as f:
        for p in entries:
            f.write(f"{sha256_file(p)}  {p.name if p.parent == out_dir else str(p)}\n")
    print(f'Wrote: {sums_path}')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
