#!/usr/bin/env python3
"""Generate a reproducible local QC proof bundle for an MP4 without committing the media.

The bundle captures lightweight metadata (ffmpeg -i and loudnorm stderr) plus hashes so the
heavy MP4 can stay out of the repo while still keeping evidence of what was reviewed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable, Sequence

import imageio_ffmpeg

REPO_ROOT = Path(__file__).resolve().parent.parent


def write_atomic_text(path: Path, content: str) -> None:
    """Write text via temp file then rename to avoid partial outputs."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = None
    try:
        tmp = tempfile.NamedTemporaryFile(
            "w", delete=False, dir=str(path.parent), encoding="utf-8", newline=""
        )
        tmp.write(content)
        tmp.close()
        os.replace(tmp.name, path)
    except Exception:
        if tmp is not None:
            try:
                os.unlink(tmp.name)
            except OSError:
                pass
        raise


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_input_label(raw_input: str, resolved: Path) -> str:
    """Prefer a repo-relative label when the input lives under the repo root."""
    try:
        return resolved.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        raw_path = Path(raw_input)
        if not raw_path.is_absolute():
            return raw_path.as_posix()
        return resolved.as_posix()


def extract_loudnorm_json(stderr: str) -> dict | None:
    """Extract the last loudnorm JSON object from ffmpeg stderr."""
    matches = re.findall(r"\{.*?\}", stderr, flags=re.DOTALL)
    for block in reversed(matches):
        try:
            obj = json.loads(block)
        except Exception:
            continue
        if isinstance(obj, dict) and (
            "input_i" in obj or "output_i" in obj or "target_offset" in obj
        ):
            return obj
    return None


def run_ffmpeg(cmd: Sequence[str]) -> tuple[int, str, str]:
    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def write_sha256sums(out_dir: Path, entries: Iterable[tuple[str, Path]]) -> Path:
    """Write SHA256SUMS.txt with deterministic ordering by label."""
    sums_path = out_dir / "SHA256SUMS.txt"
    sorted_entries = sorted(entries, key=lambda item: item[0])
    lines = [f"{sha256_file(path)}  {label}\n" for label, path in sorted_entries]
    write_atomic_text(sums_path, "".join(lines))
    return sums_path


def build_readme(
    input_label: str,
    include_ffmpeg: bool,
    loudnorm_ran: bool,
    loudnorm_parsed: bool,
    targets: tuple[str, str, str],
) -> str:
    lines: list[str] = []
    lines.append("# Local QC proof bundle\n")
    lines.append(
        f"This directory holds reproducible local QC artifacts for `{input_label}`. "
        "The MP4 itself is not committed; only lightweight logs and hashes are stored.\n"
    )
    lines.append("Captured files:\n")
    lines.append("- README.md: this overview.\n")
    if include_ffmpeg:
        lines.append("- ffmpeg_i.txt: stderr from `ffmpeg -i` (no output written).\n")
    if loudnorm_ran:
        lines.append("- loudnorm_pass_log.txt: stderr from the loudnorm analysis pass.\n")
        if loudnorm_parsed:
            lines.append(
                "- loudnorm_analysis.json: JSON snapshot parsed from loudnorm stderr (last object).\n"
            )
        else:
            lines.append(
                "- loudnorm_analysis.json: not written because loudnorm JSON parsing failed; "
                "see the log for details.\n"
            )
    lines.append("- SHA256SUMS.txt: sha256 of the input MP4 plus the files above.\n")

    if loudnorm_ran:
        target_i, target_tp, target_lra = targets
        lines.append("\n## Loudness snapshot\n")
        lines.append(
            f"Analysis targets: I={target_i}, TP={target_tp}, LRA={target_lra} (analysis-only, no output media).\n"
        )
        if loudnorm_parsed:
            lines.append(
                "Parsed loudnorm values are in `loudnorm_analysis.json`; full stderr is in `loudnorm_pass_log.txt`.\n"
            )
        else:
            lines.append(
                "Loudnorm stderr is captured in `loudnorm_pass_log.txt`, but JSON could not be parsed. "
                "This bundle still exits successfully for local QC bookkeeping.\n"
            )

    return "".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Capture a local QC proof bundle for an MP4.")
    ap.add_argument("--in", dest="input_path", required=True, help="Path to input MP4 (repo-relative or absolute)")
    ap.add_argument("--out-dir", required=True, help="Directory to write the QC bundle into")
    ap.add_argument("--target-i", default="-15", help="loudnorm target I (default: %(default)s)")
    ap.add_argument("--target-tp", default="-1.5", help="loudnorm target TP (default: %(default)s)")
    ap.add_argument("--target-lra", default="11", help="loudnorm target LRA (default: %(default)s)")
    ap.add_argument(
        "--include-ffmpeg-i",
        dest="include_ffmpeg_i",
        action="store_true",
        default=True,
        help="Capture ffmpeg -i stderr (default: true)",
    )
    ap.add_argument(
        "--no-include-ffmpeg-i",
        dest="include_ffmpeg_i",
        action="store_false",
        help="Skip ffmpeg -i capture",
    )
    ap.add_argument(
        "--skip-loudnorm",
        action="store_true",
        help="Skip the loudnorm analysis pass",
    )
    args = ap.parse_args(argv)

    raw_input_path = args.input_path
    input_path = Path(raw_input_path)
    resolved_input = input_path if input_path.is_absolute() else (Path.cwd() / input_path)
    resolved_input = resolved_input.resolve()

    if not resolved_input.exists():
        print(f"ERROR: missing input: {raw_input_path}", file=sys.stderr)
        return 2

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as e:
        print(f"ERROR: could not locate ffmpeg via imageio_ffmpeg: {e}", file=sys.stderr)
        return 1

    written_files: list[Path] = []
    loudnorm_obj: dict | None = None

    if args.include_ffmpeg_i:
        cmd_i = [ffmpeg_exe, "-nostdin", "-hide_banner", "-i", str(resolved_input)]
        _, _, err_i = run_ffmpeg(cmd_i)
        ffmpeg_i_path = out_dir / "ffmpeg_i.txt"
        write_atomic_text(ffmpeg_i_path, err_i)
        written_files.append(ffmpeg_i_path)

    if not args.skip_loudnorm:
        cmd_ln = [
            ffmpeg_exe,
            "-nostdin",
            "-hide_banner",
            "-y",
            "-i",
            str(resolved_input),
            "-af",
            f"loudnorm=I={args.target_i}:TP={args.target_tp}:LRA={args.target_lra}:print_format=json",
            "-f",
            "null",
            "-",
        ]
        _, _, err_ln = run_ffmpeg(cmd_ln)
        loudnorm_log_path = out_dir / "loudnorm_pass_log.txt"
        write_atomic_text(loudnorm_log_path, err_ln)
        written_files.append(loudnorm_log_path)

        loudnorm_obj = extract_loudnorm_json(err_ln)
        if loudnorm_obj is not None:
            loudnorm_json_path = out_dir / "loudnorm_analysis.json"
            write_atomic_text(
                loudnorm_json_path,
                json.dumps(loudnorm_obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            )
            written_files.append(loudnorm_json_path)

    input_label = normalize_input_label(raw_input_path, resolved_input)
    readme_path = out_dir / "README.md"
    readme_text = build_readme(
        input_label=input_label,
        include_ffmpeg=args.include_ffmpeg_i,
        loudnorm_ran=not args.skip_loudnorm,
        loudnorm_parsed=loudnorm_obj is not None,
        targets=(args.target_i, args.target_tp, args.target_lra),
    )
    write_atomic_text(readme_path, readme_text)
    written_files.append(readme_path)

    sha_entries = [(input_label, resolved_input)]
    for path in written_files:
        label = path.relative_to(out_dir).as_posix()
        sha_entries.append((label, path))
    write_sha256sums(out_dir, sha_entries)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
