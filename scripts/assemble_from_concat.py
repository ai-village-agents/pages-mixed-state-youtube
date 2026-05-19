#!/usr/bin/env python3
"""Assemble a narrated slide video from an ffmpeg concat-demuxer list.

This script is intentionally small and explicit. It:
  1) builds a VFR video from a concat list of still images + durations
  2) converts that VFR video to CFR 30fps
  3) muxes narration audio to produce a final MP4

By default it uses imageio-ffmpeg's bundled ffmpeg binary, which is useful
in environments where `ffmpeg` is not on PATH.

See docs/video5_build.md for context.
"""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path


def _ffmpeg_default() -> str:
    try:
        import imageio_ffmpeg  # type: ignore

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def _quote_cmd(cmd: list[str]) -> str:
    return " ".join(shlex.quote(c) for c in cmd)


def run(cmd: list[str], dry_run: bool) -> None:
    print("+", _quote_cmd(cmd))
    if dry_run:
        return
    subprocess.run(cmd, check=True)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Assemble a narrated slide MP4 from a concat list + audio."
    )
    ap.add_argument(
        "--concat",
        required=True,
        help="Path to ffmpeg concat-demuxer list (e.g., build/video5_slides_concat.txt).",
    )
    ap.add_argument(
        "--audio",
        required=True,
        help="Narration audio path (e.g., build/video5_narration.mp3).",
    )
    ap.add_argument(
        "--out",
        required=True,
        help="Output MP4 path.",
    )
    ap.add_argument(
        "--ffmpeg",
        default=_ffmpeg_default(),
        help="Optional path to ffmpeg binary (default: imageio-ffmpeg if available).",
    )
    ap.add_argument(
        "--baseline",
        action="store_true",
        help="Encode final output as H.264 Constrained Baseline + AAC 48k + faststart (Firefox end-seek workaround).",
    )
    ap.add_argument(
        "--tmp-dir",
        default=None,
        help="Optional temporary directory for intermediates (default: create under build/ when possible).",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without running ffmpeg.",
    )

    args = ap.parse_args(argv)

    ffmpeg = str(args.ffmpeg)
    concat_path = Path(args.concat)
    audio_path = Path(args.audio)
    out_path = Path(args.out)

    if not concat_path.exists():
        raise SystemExit(f"concat file not found: {concat_path}")
    if not audio_path.exists():
        raise SystemExit(f"audio file not found: {audio_path}")

    # Choose temp directory.
    if args.tmp_dir:
        tmp_dir = Path(args.tmp_dir)
        if not args.dry_run:
            tmp_dir.mkdir(parents=True, exist_ok=True)
    else:
        preferred_parent = Path("build")
        if args.dry_run:
            # Avoid filesystem side-effects on dry runs.
            if preferred_parent.exists() and preferred_parent.is_dir():
                tmp_dir = preferred_parent / "_dryrun_tmp"
            else:
                tmp_dir = Path("_dryrun_tmp")
        else:
            if preferred_parent.exists() and preferred_parent.is_dir():
                tmp_dir = Path(
                    tempfile.mkdtemp(prefix="assemble_tmp_", dir=str(preferred_parent))
                )
            else:
                tmp_dir = Path(tempfile.mkdtemp(prefix="assemble_tmp_"))

    vfr_mp4 = tmp_dir / "video_vfr.mp4"
    cfr_mp4 = tmp_dir / "video_cfr30.mp4"

    # 1) concat -> VFR
    # Important: keep this VFR; do NOT force fps here.
    cmd_vfr = [
        ffmpeg,
        "-hide_banner",
        "-y",
        "-nostdin",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_path),
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-crf",
        "20",
        "-preset",
        "veryfast",
        "-fps_mode",
        "vfr",
        str(vfr_mp4),
    ]

    # 2) VFR -> CFR30
    cmd_cfr = [
        ffmpeg,
        "-hide_banner",
        "-y",
        "-nostdin",
        "-i",
        str(vfr_mp4),
        "-an",
        "-vf",
        "fps=30",
        "-fps_mode",
        "cfr",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-crf",
        "20",
        "-preset",
        "veryfast",
        str(cfr_mp4),
    ]

    # 3) Mux audio -> final
    if not args.dry_run:
        out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.baseline:
        cmd_out = [
            ffmpeg,
            "-hide_banner",
            "-y",
            "-nostdin",
            "-i",
            str(cfr_mp4),
            "-i",
            str(audio_path),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-profile:v",
            "baseline",
            "-level",
            "4.0",
            "-crf",
            "20",
            "-preset",
            "veryfast",
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            "-ar",
            "48000",
            "-ac",
            "1",
            "-shortest",
            "-movflags",
            "+faststart",
            str(out_path),
        ]
    else:
        cmd_out = [
            ffmpeg,
            "-hide_banner",
            "-y",
            "-nostdin",
            "-i",
            str(cfr_mp4),
            "-i",
            str(audio_path),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            "-ar",
            "48000",
            "-ac",
            "1",
            "-shortest",
            "-movflags",
            "+faststart",
            str(out_path),
        ]

    print(f"Temp dir: {tmp_dir}")
    run(cmd_vfr, args.dry_run)
    run(cmd_cfr, args.dry_run)
    run(cmd_out, args.dry_run)

    if args.dry_run:
        return 0

    print(f"Wrote: {out_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        raise SystemExit(130)
