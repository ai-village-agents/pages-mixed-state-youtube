"""Generate a simple slide montage/contact sheet.

Example:
  python slides/make_montage.py slides/rendered_video5

Writes <dir>/_montage.png by default.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Create a montage (_montage.png) from rendered slide PNGs.")
    p.add_argument("dir", type=str, help="Directory containing slide_XX.png files")
    p.add_argument("--pattern", default="slide_*.png", help="Glob pattern for slide images")
    p.add_argument("--cols", type=int, default=5, help="Number of columns")
    p.add_argument("--thumb-scale", type=int, default=4, help="Downscale factor for thumbnails (1920/scale)")
    p.add_argument("--pad", type=int, default=16, help="Padding between tiles (px)")
    p.add_argument("--bg", default="#0b1020", help="Background color (hex)")
    p.add_argument("--out", default=None, help="Output path (default: <dir>/_montage.png)")
    return p.parse_args()


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    s = hex_color.strip()
    if s.startswith("#"):
        s = s[1:]
    if len(s) != 6:
        raise ValueError(f"Expected 6-digit hex color, got: {hex_color!r}")
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


def main() -> None:
    args = parse_args()
    in_dir = Path(args.dir)
    if not in_dir.exists() or not in_dir.is_dir():
        raise SystemExit(f"Not a directory: {in_dir}")

    slides = sorted(in_dir.glob(args.pattern))
    if not slides:
        raise SystemExit(f"No images matched {args.pattern!r} in {in_dir}")

    # Determine base size from the first image
    first = Image.open(slides[0]).convert("RGB")
    base_w, base_h = first.size
    scale = max(1, int(args.thumb_scale))
    thumb_w, thumb_h = base_w // scale, base_h // scale

    cols = max(1, int(args.cols))
    rows = math.ceil(len(slides) / cols)
    pad = max(0, int(args.pad))
    bg = hex_to_rgb(args.bg)

    mont_w = pad + cols * (thumb_w + pad)
    mont_h = pad + rows * (thumb_h + pad)
    montage = Image.new("RGB", (mont_w, mont_h), bg)

    for i, path in enumerate(slides):
        img = Image.open(path).convert("RGB")
        thumb = img.resize((thumb_w, thumb_h), resample=Image.BICUBIC)
        r = i // cols
        c = i % cols
        x = pad + c * (thumb_w + pad)
        y = pad + r * (thumb_h + pad)
        montage.paste(thumb, (x, y))

    out_path = Path(args.out) if args.out else (in_dir / "_montage.png")
    montage.save(out_path, format="PNG")
    print(f"Wrote {out_path} ({len(slides)} slides, {cols} cols)")


if __name__ == "__main__":
    main()
