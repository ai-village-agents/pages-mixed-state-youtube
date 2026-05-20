#!/usr/bin/env python3
"""qc_contact_sheet_midpoints.py

Generate a midpoint contact sheet for a slide-based video.

Given:
  - an MP4 video
  - an ffmpeg concat timing file containing repeating pairs:
      file '/abs/path/to/slide.png'
      duration 12.345
    (often ending with a trailing `file ...` line without a duration)

This script extracts one frame at the midpoint of each timed segment and
assembles them into a labeled contact sheet grid.

Example:
  python scripts/qc_contact_sheet_midpoints.py \
    --video build/video6/video6_upload_candidate_final_loud.mp4 \
    --concat build/video6/video6_slides_concat_final.txt \
    --out build/video6/qc/video6_contact_sheet_midpoints.png

Notes:
- Uses ffmpeg with -nostdin and quiet logging.
- Uses ImageMagick (convert + montage) for labeling and grid assembly.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass(frozen=True)
class Segment:
    index: int  # 1-based
    slide_path: str
    duration: float
    midpoint: float


FILE_RE = re.compile(r"^file\s+'(.*)'\s*$")
DUR_RE = re.compile(r"^duration\s+([0-9]*\.?[0-9]+)\s*$")


def _die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


def which_or_none(cmd: str) -> Optional[str]:
    return shutil.which(cmd)


def find_ffmpeg() -> str:
    ff = which_or_none("ffmpeg")
    if ff:
        return ff
    try:
        import imageio_ffmpeg  # type: ignore

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as e:
        _die(
            "Could not find 'ffmpeg' on PATH and imageio_ffmpeg fallback failed: "
            f"{e}"
        )
    raise AssertionError("unreachable")


def parse_concat_timing(path: Path) -> List[Segment]:
    if not path.exists():
        _die(f"Concat file not found: {path}")
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines()]
    pending_file: Optional[str] = None

    segs: List[Segment] = []
    t = 0.0
    for ln in lines:
        if not ln or ln.startswith("#"):
            continue
        mfile = FILE_RE.match(ln)
        if mfile:
            pending_file = mfile.group(1)
            continue
        mdur = DUR_RE.match(ln)
        if mdur:
            if pending_file is None:
                _die(
                    f"Found duration with no preceding file line in {path}: {ln}"
                )
            dur = float(mdur.group(1))
            if dur <= 0:
                _die(f"Non-positive duration {dur} for file {pending_file}")
            mid = t + dur / 2.0
            segs.append(
                Segment(index=len(segs) + 1, slide_path=pending_file, duration=dur, midpoint=mid)
            )
            t += dur
            pending_file = None
            continue

        # Unknown line
        _die(f"Unrecognized line in concat file {path}: {ln}")

    # Common pattern: a trailing `file '...'` with no duration. Ignore it.
    if pending_file is not None:
        # ignore
        pending_file = None

    if not segs:
        _die(f"No segments parsed from concat file: {path}")
    return segs


def format_timestamp_mmssxx(seconds: float) -> str:
    if seconds < 0:
        seconds = 0.0
    m = int(seconds // 60)
    s = seconds - 60 * m
    # two decimals, always 2 digits seconds
    return f"{m:02d}:{s:05.2f}"


def run(cmd: List[str]) -> None:
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        _die(f"Command failed (exit {e.returncode}): {' '.join(cmd)}")


def ensure_parent(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="Make a midpoint contact sheet from a concat timing file.")
    ap.add_argument("--video", required=True, help="Input MP4 video path")
    ap.add_argument("--concat", required=True, help="ffmpeg concat timing file")
    ap.add_argument("--out", required=True, help="Output contact sheet PNG")
    ap.add_argument(
        "--frames-dir",
        default=None,
        help="Directory to write extracted frames (default: alongside --out in frames_midpoints/)",
    )
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--rows", type=int, default=3)
    ap.add_argument("--thumb-width", type=int, default=640)
    ap.add_argument("--font-size", type=int, default=28)
    ap.add_argument("--label-gravity", default="SouthWest")
    ap.add_argument("--label-pad-x", type=int, default=12)
    ap.add_argument("--label-pad-y", type=int, default=12)

    args = ap.parse_args()

    video = Path(args.video)
    concat = Path(args.concat)
    out = Path(args.out)

    if not video.exists():
        _die(f"Video not found: {video}")
    if args.cols <= 0 or args.rows <= 0:
        _die("--cols and --rows must be positive")
    if args.thumb_width <= 0:
        _die("--thumb-width must be positive")

    segs = parse_concat_timing(concat)

    frames_dir = Path(args.frames_dir) if args.frames_dir else out.parent / "frames_midpoints"
    frames_dir.mkdir(parents=True, exist_ok=True)

    ffmpeg = find_ffmpeg()

    manifest = {
        "video": str(video),
        "concat": str(concat),
        "segments": [
            {
                "index": s.index,
                "slide_path": s.slide_path,
                "duration": s.duration,
                "midpoint": s.midpoint,
                "midpoint_label": format_timestamp_mmssxx(s.midpoint),
            }
            for s in segs
        ],
    }
    (frames_dir / "frames_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8"
    )

    # Extract frames
    extracted: List[Path] = []
    for s in segs:
        frame_path = frames_dir / f"frame_S{s.index:02d}.png"
        # -ss before -i is fast seek; acceptable for QC.
        cmd = [
            ffmpeg,
            "-nostdin",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-ss",
            f"{s.midpoint:.3f}",
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-vf",
            f"scale={args.thumb_width}:-2",
            str(frame_path),
        ]
        run(cmd)
        if not frame_path.exists():
            _die(f"Expected frame not created: {frame_path}")
        extracted.append(frame_path)

    convert = which_or_none("convert")
    montage = which_or_none("montage")
    if not (convert and montage):
        _die(
            "ImageMagick not available (need 'convert' and 'montage' on PATH). "
            f"Extracted frames are in: {frames_dir}"
        )

    labeled_dir = frames_dir / "labeled"
    labeled_dir.mkdir(parents=True, exist_ok=True)

    labeled_paths: List[Path] = []
    for s, frame_path in zip(segs, extracted):
        label = f"S{s.index:02d} {format_timestamp_mmssxx(s.midpoint)}"
        labeled_path = labeled_dir / frame_path.name
        # Outline text for readability: draw stroke then fill.
        # Using +pad offsets with gravity.
        annotate = f"+{args.label_pad_x}+{args.label_pad_y}"
        cmd = [
            convert,
            str(frame_path),
            "-gravity",
            args.label_gravity,
            "-pointsize",
            str(args.font_size),
            "-stroke",
            "black",
            "-strokewidth",
            "3",
            "-fill",
            "white",
            "-annotate",
            annotate,
            label,
            "-stroke",
            "none",
            "-fill",
            "white",
            "-annotate",
            annotate,
            label,
            str(labeled_path),
        ]
        run(cmd)
        labeled_paths.append(labeled_path)

    ensure_parent(out)
    # Montage into grid
    tile = f"{args.cols}x{args.rows}"
    cmd = [
        montage,
        *[str(p) for p in labeled_paths],
        "-tile",
        tile,
        "-geometry",
        "+8+8",
        "-background",
        "#111111",
        "-bordercolor",
        "#111111",
        str(out),
    ]
    run(cmd)

    if not out.exists():
        _die(f"Expected contact sheet not created: {out}")

    print(f"Wrote contact sheet: {out}")
    print(f"Frames + manifest: {frames_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
