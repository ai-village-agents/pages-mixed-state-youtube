"""Generate deterministic resized preview PNGs next to source images.

Example:
  python slides/make_previews.py slides/rendered_video7/slide_05.png slides/rendered_video7/_montage.png
"""

from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path
from typing import Iterable

from PIL import Image

DEFAULT_SIZES = "320x180,640x360"

RESAMPLE_MAP = {
    "nearest": Image.NEAREST,
    "bilinear": Image.BILINEAR,
    "bicubic": Image.BICUBIC,
    "lanczos": Image.LANCZOS,
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate resized preview PNGs next to source images.")
    p.add_argument("images", nargs="+", help="Input image path(s)")
    p.add_argument(
        "--sizes",
        default=DEFAULT_SIZES,
        help="Comma-separated list of sizes like '320x180,640x360'",
    )
    p.add_argument(
        "--suffix-format",
        default="_preview_{w}x{h}.png",
        help="Filename suffix format (uses {w} and {h}) appended to the stem",
    )
    p.add_argument(
        "--resample",
        choices=sorted(RESAMPLE_MAP),
        default="bicubic",
        help="Resampling method",
    )
    return p.parse_args()


def parse_sizes(raw: str) -> list[tuple[int, int]]:
    sizes: list[tuple[int, int]] = []
    for chunk in raw.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "x" not in chunk.lower():
            raise ValueError(f"Size must be <w>x<h>, got {chunk!r}")
        w_str, h_str = chunk.lower().split("x", 1)
        try:
            w, h = int(w_str), int(h_str)
        except ValueError as exc:
            raise ValueError(f"Size must be integers, got {chunk!r}") from exc
        if w <= 0 or h <= 0:
            raise ValueError(f"Size must be positive, got {chunk!r}")
        sizes.append((w, h))
    return sizes


def save_png_atomic(image: Image.Image, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    temp_file = tempfile.NamedTemporaryFile(dir=dest.parent, suffix=".tmp", delete=False)
    temp_path = Path(temp_file.name)
    temp_file.close()
    try:
        image.save(temp_path, format="PNG")
        os.replace(temp_path, dest)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def build_output_path(src: Path, suffix_fmt: str, w: int, h: int) -> Path:
    try:
        suffix = suffix_fmt.format(w=w, h=h)
    except (KeyError, ValueError) as exc:
        raise SystemExit(f"Invalid --suffix-format: {exc}") from exc
    return src.with_name(src.stem + suffix)


def make_previews(
    src: Path,
    sizes: Iterable[tuple[int, int]],
    suffix_fmt: str,
    resample: int,
) -> list[Path]:
    with Image.open(src) as img:
        rgb = img.convert("RGB")
        written: list[Path] = []
        for w, h in sizes:
            resized = rgb.resize((w, h), resample=resample)
            out_path = build_output_path(src, suffix_fmt, w, h)
            save_png_atomic(resized, out_path)
            written.append(out_path)
    return written


def main() -> None:
    args = parse_args()

    try:
        sizes = parse_sizes(args.sizes)
    except ValueError as exc:
        raise SystemExit(f"Invalid --sizes: {exc}") from exc
    if not sizes:
        raise SystemExit("No sizes provided after parsing --sizes")

    resample = RESAMPLE_MAP[args.resample]
    suffix_fmt = args.suffix_format

    for image_path in args.images:
        src = Path(image_path)
        if not src.exists():
            raise SystemExit(f"Not found: {src}")
        written = make_previews(src, sizes, suffix_fmt, resample)
        for out_path in written:
            print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
