#!/usr/bin/env python3
"""Build a legibility mosaic from slide preview thumbnails."""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Iterable, List, Tuple

from PIL import Image

SLIDE_RE = re.compile(r"^slide_(\d+)")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Build a legibility mosaic from slide previews.")
    ap.add_argument("--previews-dir", default="slides/rendered_video7", help="Directory containing slide_* preview PNGs")
    ap.add_argument("--out", default="artifacts/video7/qc/legibility_mosaic_320x180.png", help="Output mosaic path")
    ap.add_argument("--suffix", default="_preview_320x180.png", help="Suffix used to pick preview files (default: %(default)s)")
    ap.add_argument("--cols", type=int, default=5, help="Number of columns in the mosaic (default: %(default)s)")
    ap.add_argument("--rows", type=int, default=2, help="Number of rows in the mosaic (default: %(default)s)")
    ap.add_argument(
        "--count",
        type=int,
        help="Number of slides to include (default: cols*rows)",
    )
    return ap.parse_args(argv)


def user_error(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 2


def find_slides(previews_dir: Path, suffix: str) -> List[Tuple[int, Path]]:
    """Return [(slide_number, path), ...] sorted by slide number."""
    matches: list[tuple[int, Path]] = []
    for path in sorted(previews_dir.glob(f"slide_*{suffix}")):
        m = SLIDE_RE.match(path.name)
        if not m:
            continue
        matches.append((int(m.group(1)), path))
    matches.sort(key=lambda pair: pair[0])
    return matches


def load_images(paths: Iterable[Path]) -> tuple[list[Image.Image], tuple[int, int]]:
    images: list[Image.Image] = []
    base_size: tuple[int, int] | None = None

    for path in paths:
        try:
            with Image.open(path) as im:
                img = im.copy()
        except Exception as e:  # pragma: no cover - runtime safety
            raise RuntimeError(f"Failed to open {path}: {e}") from e

        if base_size is None:
            base_size = img.size
        elif img.size != base_size:
            raise ValueError(f"Image {path} has size {img.size}, expected {base_size}")
        images.append(img)

    if base_size is None:
        raise ValueError("No images to load")

    return images, base_size


def write_atomic_image(path: Path, image: Image.Image) -> None:
    """Write a PNG atomically: temp file then replace."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = None
    try:
        tmp = tempfile.NamedTemporaryFile("wb", delete=False, dir=str(path.parent))
        with tmp:
            image.save(tmp, format="PNG")
        os.replace(tmp.name, path)
    except Exception:
        if tmp is not None:
            try:
                os.unlink(tmp.name)
            except OSError:
                pass
        raise


def build_mosaic(images: list[Image.Image], size: tuple[int, int], cols: int, rows: int) -> Image.Image:
    width, height = size
    mosaic = Image.new(images[0].mode, (cols * width, rows * height))
    for idx, img in enumerate(images):
        row = idx // cols
        col = idx % cols
        mosaic.paste(img, (col * width, row * height))
    return mosaic


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    expected_count = args.cols * args.rows
    count = expected_count if args.count is None else args.count
    if count != expected_count:
        return user_error(f"--count must equal cols*rows ({expected_count}), got {count}")

    previews_dir = Path(args.previews_dir)
    slides = find_slides(previews_dir, args.suffix)

    if len(slides) < count:
        return user_error(
            f"Expected at least {count} slides matching slide_*{args.suffix} in {previews_dir}, found {len(slides)}"
        )

    selected_paths = [path for _, path in slides[:count]]

    try:
        images, size = load_images(selected_paths)
    except ValueError as e:
        return user_error(str(e))
    except RuntimeError as e:
        return user_error(str(e))

    mosaic = build_mosaic(images, size, args.cols, args.rows)

    try:
        write_atomic_image(Path(args.out), mosaic)
    except Exception as e:  # pragma: no cover - runtime safety
        print(f"ERROR: Failed to write output: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
