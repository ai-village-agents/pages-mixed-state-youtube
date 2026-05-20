#!/usr/bin/env python3
"""chapters_from_narration_md_and_concat.py

Generate YouTube-style chapter timestamps from:
  1) a narration markdown file with headings like: "## Slide N — Title"
  2) an ffmpeg concat timing file with "duration X" lines

This helps keep chapter timestamps in sync with slide timings.

Example:
  python scripts/chapters_from_narration_md_and_concat.py \
    --narration-md script/VIDEO7_narration.md \
    --concat build/video7/video7_slides_concat_final.txt

Output:
  - Markdown bullet list suitable for YouTube description.

Notes:
- Timestamps are computed from segment *start times*.
- Formatting uses floor(seconds) to avoid producing a timestamp that starts *after*
  the true segment boundary.
"""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path


SLIDE_RE = re.compile(r"^##\s+Slide\s+(\d+)\s+—\s+(.*)$", flags=re.M)
DUR_RE = re.compile(r"^duration\s+([0-9]*\.?[0-9]+)\s*$")


def parse_slide_titles(md_text: str) -> list[tuple[int, str]]:
    slides = []
    for m in SLIDE_RE.finditer(md_text):
        n = int(m.group(1))
        title = m.group(2).strip()
        slides.append((n, title))
    if not slides:
        raise SystemExit("No slide headings found; expected lines like: '## Slide N — Title'")
    # ensure contiguous numbering
    nums = [n for n, _ in slides]
    if nums != list(range(1, len(nums) + 1)):
        raise SystemExit(f"Unexpected slide numbering: {nums}")
    return slides


def parse_durations(concat_text: str) -> list[float]:
    durs = []
    file_lines = False
    audio_file_lines = False

    for ln in concat_text.splitlines():
        ln = ln.strip()
        m = DUR_RE.match(ln)
        if m:
            d = float(m.group(1))
            if d <= 0:
                raise SystemExit(f"Non-positive duration found: {d}")
            durs.append(d)
        elif ln.lower().startswith("file "):
            file_lines = True
            path = ln[5:].strip().strip("\"'")
            if path.lower().endswith((".mp3", ".wav")):
                audio_file_lines = True
    if not durs:
        hint = (
            "This script requires an ffmpeg concat file WITH duration lines "
            "(e.g. slides concat like build/video7/video7_slides_concat_final.txt). "
        )
        if audio_file_lines:
            hint += "The provided concat looks like an audio concat (paths ending in .mp3/.wav) with only 'file ...' lines."
        elif file_lines:
            hint += "The provided concat appears to have only 'file ...' lines (typical for narration/audio concat)."
        else:
            hint += "Narration concat lists produced for audio concatenation typically have only 'file ...' lines."
        raise ValueError(f"No duration lines found in concat file. {hint}")
    return durs


def fmt_mmss(seconds: float, mode: str = "round") -> str:
    x = max(0.0, seconds)
    if mode == "floor":
        total = int(math.floor(x))
    elif mode == "ceil":
        total = int(math.ceil(x))
    elif mode == "round":
        total = int(round(x))
    else:
        raise ValueError(f"Unknown mode: {mode}")

    m = total // 60
    s = total % 60
    return f"{m}:{s:02d}"


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate chapter timestamps from narration MD + concat file")
    ap.add_argument("--narration-md", required=True, help="Narration markdown file (## Slide N — Title)")
    ap.add_argument(
        "--concat",
        required=True,
        help="ffmpeg concat file with duration lines (image/slides timeline)",
    )
    ap.add_argument(
        "--offset-seconds",
        type=float,
        default=0.0,
        help="Add a fixed offset to all timestamps (default 0.0)",
    )
    ap.add_argument(
        "--mode",
        choices=["round", "floor", "ceil"],
        default="round",
        help="How to convert fractional seconds to whole-second chapter times (default: round)",
    )
    args = ap.parse_args()

    md_path = Path(args.narration_md)
    concat_path = Path(args.concat)

    md_text = md_path.read_text(encoding="utf-8")
    concat_text = concat_path.read_text(encoding="utf-8")

    slides = parse_slide_titles(md_text)
    try:
        durs = parse_durations(concat_text)
    except ValueError as exc:
        raise SystemExit(exc) from exc

    if len(durs) != len(slides):
        raise SystemExit(
            f"Mismatch: {len(slides)} slides in {md_path} but {len(durs)} duration lines in {concat_path}"
        )

    t = float(args.offset_seconds)
    for (n, title), _dur in zip(slides, durs):
        print(f"- {fmt_mmss(t, args.mode)} {title}")
        t += _dur

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
