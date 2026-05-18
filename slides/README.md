# Slides

Slide text lives in `slide_text.yaml`.

## Render PNGs

```bash
pip install pillow pyyaml
python slides/render_slides.py --input slides/slide_text.yaml --output-dir slides/rendered
```

Outputs: `slides/rendered/slide_01.png`, `slide_02.png`, ...

Notes:
- 1920×1080, dark background, teal titles.
- Uses DejaVu fonts if available; falls back to default fonts.
