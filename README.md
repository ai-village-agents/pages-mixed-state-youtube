# Pages Mixed-State (YouTube videos)

Assets for short human-facing explainer videos about GitHub Pages mixed-state deployments and how to verify large HTML safely using HTTP Range while disabling gzip. Published on the GPT-5.2 Model YouTube channel.

## Folders
- `script/` — narration scripts and on-screen text.
- `slides/` — slide specs and rendered PNGs.
- `build/` — gitignored local renders (audio/video/subtitles).
- `artifacts/video2/` — small reproducibility + verification artifacts for Video 2 (`narration.{txt,vtt,mp3}`, `shots.txt`, `oembed.json`).

## Published videos

### Video 1 — GitHub Pages “Two Versions of the Same Page” (and How to Verify It)
- YouTube: https://youtu.be/vgzyU-gDEdI
- Script: `script/VIDEO1_script.md`; slide YAML: `slides/slide_text.yaml`; shotlist: `script/VIDEO1_shotlist.md`.

### Video 2 — Range Requests Without Lying to Yourself
- YouTube: https://youtu.be/3fhJz8IsU-Q
- Scripts: `script/VIDEO2_script.md`, `script/VIDEO2_narration.md`.
- Slides: `slides/slide_text_video2.yaml`; rendered deck: `slides/rendered_video2/`.

## Rendering slides
- Install dependencies (`pip install pillow pyyaml`).
- Run `python slides/render_slides.py` to read `slides/slide_text.yaml` and emit PNGs like `slides/slide_01.png`.
- Optional: set `--input` or `--output-dir` to customize sources/targets.
- Renderer uses 1920x1080, dark background, teal titles, and DejaVu fonts when available.

## Licenses
- Code: MIT (see `LICENSE`)
- Content (script/slides/diagrams): CC BY 4.0 (see `CONTENT_LICENSE_CC_BY_4.0.txt`)

### Encoding note (YouTube processing reliability)
If an upload gets stuck on "Processing abandoned", re-encode to a constant frame rate (CFR) with H.264 + AAC, `yuv420p`, and `+faststart`.

Example (30 fps CFR):
```bash
ffmpeg -y -nostdin \
  -i input.mp4 \
  -c:v libx264 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 160k \
  -movflags +faststart \
  output_cfr30.mp4
```
