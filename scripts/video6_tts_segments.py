#!/usr/bin/env python3
"""Generate per-slide edge-tts MP3 segments from script/VIDEO6_narration.md.

Why: We want accurate per-slide durations WITHOUT speaking "Slide 1" cues.

Outputs (gitignored):
- build/video6/segments/slide_01.mp3 .. slide_12.mp3
- build/video6/video6_narration_brian_final.mp3
- build/video6/video6_slides_concat_final.txt

Then you can assemble via:
  python scripts/assemble_from_concat.py --concat build/video6/video6_slides_concat_final.txt \
    --audio build/video6/video6_narration_brian_final.mp3 --out build/video6/video6_upload_candidate_final.mp4 --baseline
"""

import argparse
import asyncio
import hashlib
import json
import re
from pathlib import Path
import subprocess

DEFAULT_VOICE = "en-US-BrianNeural"
MD_PATH = Path("script/VIDEO6_narration.md")
OUT_DIR = Path("build/video6")
SEG_DIR = OUT_DIR / "segments"
MANIFEST_PATH = SEG_DIR / "segments_manifest.json"

# Use imageio-ffmpeg binary so we don't depend on PATH ffmpeg.
def get_ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def parse_markdown_slides(md_text: str):
    """Return list of dicts: {n:int, title:str, text:str}."""
    # Split on headings like: ## Slide 1 — Title
    # Keep heading lines for title.
    parts = re.split(r"^##\s+Slide\s+(\d+)\s+—\s+(.*)$", md_text, flags=re.M)
    # parts structure: [preamble, n1, title1, body1, n2, title2, body2, ...]
    if len(parts) < 4:
        raise ValueError("Could not parse slides from markdown; expected headings like '## Slide N — ...'")

    slides = []
    for i in range(1, len(parts), 3):
        n = int(parts[i])
        title = parts[i + 1].strip()
        body = parts[i + 2].strip()
        slides.append({"n": n, "title": title, "body": body})

    # Clean body for TTS
    def clean(s: str) -> str:
        # Remove inline code backticks but keep contents
        s = re.sub(r"`([^`]*)`", r"\1", s)
        # Remove markdown headings if any slipped in
        s = re.sub(r"^#+\s+.*$", "", s, flags=re.M)
        # Collapse multiple spaces but keep paragraph breaks
        s = re.sub(r"[ \t]+", " ", s)
        # Normalize smart quotes/dashes to ASCII-ish to avoid odd pronunciation pauses
        s = s.replace("—", "-")
        # Keep paragraph breaks
        s = re.sub(r"\n{3,}", "\n\n", s)
        return s.strip()

    out = []
    for s in slides:
        text = clean(s["body"])
        if not text:
            raise ValueError(f"Slide {s['n']} has empty body")
        out.append({"n": s["n"], "title": s["title"], "text": text})

    # Ensure slide numbers are contiguous starting at 1
    nums = [s["n"] for s in out]
    if nums != list(range(1, len(nums) + 1)):
        raise ValueError(f"Unexpected slide numbering: {nums}")

    return out


def slide_hash(voice: str, text: str) -> str:
    h = hashlib.sha256()
    h.update(f"{voice}\n{text}".encode("utf-8"))
    return h.hexdigest()


async def synth_to_mp3(text: str, voice: str, out_path: Path):
    import edge_tts
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(str(out_path))


def mp3_duration_seconds(mp3_path: Path) -> float:
    ffmpeg = get_ffmpeg()
    # ffmpeg prints duration to stderr
    p = subprocess.run(
        [ffmpeg, "-hide_banner", "-nostdin", "-i", str(mp3_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", p.stderr)
    if not m:
        raise RuntimeError(f"Could not parse duration from ffmpeg output for {mp3_path}\n{p.stderr[:500]}")
    h = int(m.group(1))
    mi = int(m.group(2))
    s = float(m.group(3))
    return h * 3600 + mi * 60 + s


def concat_audio(mp3_paths, out_mp3: Path):
    ffmpeg = get_ffmpeg()
    lst = out_mp3.with_suffix(".concat.txt")
    lines = [f"file '{p.resolve().as_posix()}'" for p in mp3_paths]
    lst.write_text("\n".join(lines) + "\n", encoding="utf-8")
    cmd = [
        ffmpeg,
        "-hide_banner",
        "-y",
        "-nostdin",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(lst),
        "-c",
        "copy",
        str(out_mp3),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        stderr_preview = (result.stderr or "")[:800]
        raise RuntimeError(f"ffmpeg concat failed: {cmd}\nstderr (truncated):\n{stderr_preview}")


def write_slide_concat(slides, durations, out_txt: Path, images_dir: Path):
    base = Path('.').resolve()
    lines = []
    for n, dur in zip([s["n"] for s in slides], durations):
        img = (base / images_dir / f"slide_{n:02d}.png").resolve()
        lines.append(f"file '{img.as_posix()}'")
        lines.append(f"duration {dur:.3f}")
    # repeat last file
    last_img = (base / images_dir / f"slide_{slides[-1]['n']:02d}.png").resolve()
    lines.append(f"file '{last_img.as_posix()}'")
    out_txt.write_text("\n".join(lines) + "\n", encoding="utf-8")


async def main():
    parser = argparse.ArgumentParser(description="Generate per-slide edge-tts MP3 segments for video 6.")
    parser.add_argument("--force", action="store_true", help="Resynthesize all slide segments.")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="edge-tts voice to use.")
    parser.add_argument(
        "--padding-seconds",
        type=float,
        default=0.15,
        help="Extra seconds to add to each slide duration.",
    )
    args = parser.parse_args()

    voice = args.voice
    padding_seconds = args.padding_seconds

    md = MD_PATH.read_text(encoding="utf-8")
    slides = parse_markdown_slides(md)

    SEG_DIR.mkdir(parents=True, exist_ok=True)

    manifest = None
    if not args.force and MANIFEST_PATH.exists():
        try:
            manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            manifest = None
    manifest_slides = {s["n"]: s for s in manifest.get("slides", [])} if manifest else {}

    # Synthesize segments sequentially (avoid hammering service)
    mp3s = []
    manifest_entries = []
    for s in slides:
        out_mp3 = SEG_DIR / f"slide_{s['n']:02d}.mp3"
        mp3s.append(out_mp3)
        current_hash = slide_hash(voice, s["text"])

        existing_entry = manifest_slides.get(s["n"])
        has_match = (
            existing_entry
            and existing_entry.get("text_sha256") == current_hash
            and existing_entry.get("mp3_filename") == out_mp3.name
            and out_mp3.exists()
            and out_mp3.stat().st_size > 0
        )

        if not has_match:
            await synth_to_mp3(s["text"], voice, out_mp3)

        manifest_entries.append(
            {
                "n": s["n"],
                "title": s["title"],
                "text_sha256": current_hash,
                "mp3_filename": out_mp3.name,
            }
        )

    # Compute per-slide durations
    durations = [mp3_duration_seconds(p) for p in mp3s]

    # Build full narration mp3
    full_mp3 = OUT_DIR / "video6_narration_brian_final.mp3"
    concat_audio(mp3s, full_mp3)

    # Write slide concat list with durations (tight). Add a small padding to each slide.
    # We pad slightly so audio doesn't clip at slide boundaries.
    padded = [d + padding_seconds for d in durations]
    concat_txt = OUT_DIR / "video6_slides_concat_final.txt"
    write_slide_concat(slides, padded, concat_txt, Path("slides/rendered_video6"))

    manifest_data = {
        "voice": voice,
        "padding_seconds": padding_seconds,
        "slides": manifest_entries,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")

    total = sum(padded)
    print("Wrote:")
    print(" -", full_mp3)
    print(" -", concat_txt)
    print("Total padded slide time:", round(total, 3), "seconds")


if __name__ == "__main__":
    asyncio.run(main())
