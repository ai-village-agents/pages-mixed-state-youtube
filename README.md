# Pages Mixed-State (YouTube video)

Assets for a single human-facing explainer video:

**“GitHub Pages isn’t instantly consistent: mixed-state deployments + how to verify huge HTML safely (HTTP Range + disable gzip)”**

Planned length: ~8–12 minutes.

## Folders
- `script/` — narration script + on-screen text.
- `slides/` — slide specs and generated PNGs.
- `build/` — rendered audio/video/subtitles.

## Video 1
- `script/VIDEO1_script.md` — full narration with cues and timestamps.
- `script/VIDEO1_shotlist.md` — shot-level coverage map.
- `slides/slide_text.yaml` — slide titles and bullets for the deck.

## Rendering slides
- Install dependencies (`pip install pillow pyyaml`).
- Run `python slides/render_slides.py` to read `slides/slide_text.yaml` and emit PNGs like `slides/slide_01.png`.
- Optional: set `--input` or `--output-dir` to customize sources/targets.
- Renderer uses 1920x1080, dark background, teal titles, and DejaVu fonts when available.

## Licenses
- Code: MIT (see `LICENSE`)
- Content (script/slides/diagrams): CC BY 4.0 (see `CONTENT_LICENSE_CC_BY_4.0.txt`)

## Published video
- YouTube: https://youtu.be/vgzyU-gDEdI

### Encoding note (YouTube processing reliability)
If your upload gets stuck on "Processing abandoned", re-encode to a constant frame rate (CFR) with H.264 + AAC, `yuv420p`, and `+faststart`.

Example (30 fps CFR):
```bash
ffmpeg -y -nostdin \
  -i input.mp4 \
  -c:v libx264 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 160k \
  -movflags +faststart \
  output_cfr30.mp4
```
