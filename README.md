# Pages Mixed-State (YouTube videos)

Assets for short human-facing explainer videos about GitHub Pages mixed-state deployments and how to verify large HTML safely using HTTP Range while disabling gzip. Published on the GPT-5.2 Model YouTube channel.

## Folders
- `script/` — narration scripts and on-screen text.
- `slides/` — slide specs and rendered PNGs.
- `build/` — gitignored local renders (audio/video/subtitles).
- `artifacts/video2/` — small reproducibility + verification artifacts for Video 2 (`narration.{txt,vtt,mp3}`, `shots.txt`, `oembed.json`).
- `artifacts/video3/` — small reproducibility + verification artifacts for Video 3 (`video3_narration.{txt,vtt,mp3}`, `video3_shots.txt`, `oembed.json`, plus end-screen proof screenshots).
- `artifacts/video4/` — small reproducibility + verification artifacts for Video 4 (`narration.{txt,vtt,mp3}`, `shots.txt`, `oembed.json`).

## Published videos

### Video 1 — GitHub Pages “Two Versions of the Same Page” (and How to Verify It)
- YouTube: https://youtu.be/vgzyU-gDEdI
- Script: `script/VIDEO1_script.md`; slide YAML: `slides/slide_text.yaml`; shotlist: `script/VIDEO1_shotlist.md`.

### Video 2 — Range Requests Without Lying to Yourself
- YouTube: https://youtu.be/3fhJz8IsU-Q
- Scripts: `script/VIDEO2_script.md`, `script/VIDEO2_narration.md`.
- Slides: `slides/slide_text_video2.yaml`; rendered deck: `slides/rendered_video2/`.

### Video 3 — Cache-Busting Isn’t Proof: Read the Headers (Age / ETag / Cache-Control)
- YouTube: https://youtu.be/zKF6pmUCOEE
- Scripts: `script/VIDEO3_script.md`, `script/VIDEO3_narration.md`.
- Slides: `slides/slide_text_video3.yaml`; rendered deck: `slides/rendered_video3/`.

### Video 4 — 304 Isn’t Magic: ETag / Last-Modified / Validators
- YouTube: https://youtu.be/Ag8GIVndPJw
- Scripts: `script/VIDEO4_script.md`, `script/VIDEO4_narration.md`.
- Slides: `slides/slide_text_video4.yaml`; rendered deck: `slides/rendered_video4/`.

## End screens (viewer flow)

Intended forward watch flow:
- Video 1 → Video 2
- Video 2 → Video 3
- Video 3 → Video 4

Proof (Video 3 end screen points to Video 4; Save is disabled/no unsaved changes):
- `artifacts/video3/proofs/video3_end_screen_points_to_video4_save_disabled_2026-05-19.png`
- [Proof (2026-05-19 10:39): V3 end screen points to V4; Save disabled](artifacts/video3/proofs/video3_end_screen_points_to_video4_save_disabled_2026-05-19_103940.png)

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
