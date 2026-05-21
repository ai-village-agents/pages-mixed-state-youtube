# Slides

Slide text lives in `slide_text.yaml`.

## Render PNGs

```bash
pip install pillow pyyaml
python slides/render_slides.py --input slides/slide_text.yaml --output-dir slides/rendered
```

Outputs: `slides/rendered/slide_01.png`, `slide_02.png`, ...

Notes:
- YAML tip: if a bullet contains a colon (e.g. `Cache-Control: no-cache`) and you want plain text, wrap the whole bullet in quotes to avoid YAML treating it like a mapping.
- Optional: generate a quick contact sheet montage for a rendered deck:
  ```bash
  python slides/make_montage.py slides/rendered_video5
  ```
- Optional: generate PNG previews next to a slide or montage:
  ```bash
  python slides/make_previews.py slides/rendered_video7/slide_05.png slides/rendered_video7/_montage.png
  ```
- 1920×1080, dark background, teal titles.
- Uses DejaVu fonts if available; falls back to default fonts.

Video 2 can be rendered without touching Video 1 outputs:

```bash
python slides/render_slides.py --input slides/slide_text_video2.yaml --output-dir slides/rendered_video2
```
