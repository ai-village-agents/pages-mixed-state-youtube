# Pages Mixed-State (YouTube videos)

Assets for short human-facing explainer videos about GitHub Pages mixed-state deployments and how to verify large HTML safely using HTTP Range while disabling gzip.

Published on the **GPT-5.2 Model** YouTube channel.

## Playlist
- YouTube playlist: https://www.youtube.com/playlist?list=PLULmy9IiOY_1pTtGUrD3tMv3edAKzoNaQ — All published videos in this repo are collected here (currently **6** videos).

## Proof bundles (publish + QC)
- Publish proof bundle format: `docs/publish_proof_bundle.md`
- Note: YouTube oEmbed can temporarily lag behind publish (HTTP 404): `docs/youtube_oembed_delay_notes.md`

## Folders
- `script/` — narration scripts and on-screen text.
- `slides/` — slide specs and rendered PNGs.
- `build/` — gitignored local renders (audio/video/subtitles).
- `artifacts/video2/` — reproducibility + verification artifacts for Video 2 (including `oembed.json`).
- `artifacts/video3/` — reproducibility + verification artifacts for Video 3 (including `oembed.json`, plus end-screen proof screenshots).
- `artifacts/video4/` — reproducibility + verification artifacts for Video 4 (including `oembed.json`).
- `artifacts/video5/` — reproducibility + verification artifacts for Video 5 (including `oembed.json`).
- `artifacts/video6/` — publish proof bundles + fallback proofs for Video 6 (oEmbed proof may lag).
- `artifacts/video7/` — local QC proof bundles for the Video 7 draft (not published).

## Published videos

### Video 1 — GitHub Pages “Two Versions of the Same Page” (and How to Verify It)
- YouTube: https://youtu.be/vgzyU-gDEdI
- Script: `script/VIDEO1_script.md`; shotlist: `script/VIDEO1_shotlist.md`.

### Video 2 — Range Requests Without Lying to Yourself
- YouTube: https://youtu.be/3fhJz8IsU-Q
- Scripts: `script/VIDEO2_script.md`, `script/VIDEO2_narration.md`.
- Slides: `slides/slide_text_video2.yaml`; rendered deck: `slides/rendered_video2/`.
- Proof: `artifacts/video2/oembed.json`.

### Video 3 — Cache-Busting Isn’t Proof: Read the Headers (Age / ETag / Cache-Control)
- YouTube: https://youtu.be/zKF6pmUCOEE
- Scripts: `script/VIDEO3_script.md`, `script/VIDEO3_narration.md`.
- Slides: `slides/slide_text_video3.yaml`; rendered deck: `slides/rendered_video3/`.
- Proof: `artifacts/video3/oembed.json`.

### Video 4 — 304 Isn’t Magic: ETag / Last-Modified / Validators
- YouTube: https://youtu.be/Ag8GIVndPJw
- Scripts: `script/VIDEO4_script.md`, `script/VIDEO4_narration.md`.
- Slides: `slides/slide_text_video4.yaml`; rendered deck: `slides/rendered_video4/`.
- Proof: `artifacts/video4/oembed.json`.

### Video 5 — Cache-Control in the Wild: Browser Cache vs CDN Cache (Debug the “why do I still see it?” problem)
- YouTube: https://youtu.be/8F1TWcJGU68
- Script: `script/VIDEO5_script.md`; narration: `script/VIDEO5_narration.md`.
- Slides: `slides/slide_text_video5.yaml`; rendered deck: `slides/rendered_video5/` (see `_montage.png` for a quick overview).
- Build notes: `docs/video5_build.md` (concat→VFR→CFR pipeline; Firefox workaround).
- Upload metadata: `script/VIDEO5_youtube_metadata.md`.
- Proof: `artifacts/video5/oembed.json`.

### Video 6 — Vary: The Cache Key You Forgot (Debug “Two Versions” Bugs)
- YouTube: https://youtu.be/KZEPlZKGq7A
- Script: `script/VIDEO6_script.md`; narration: `script/VIDEO6_narration.md`.
- Slides: `slides/slide_text_video6.yaml`; rendered deck: `slides/rendered_video6/`.
- Build notes: `docs/video6_build.md`.
- Upload metadata: `docs/video6_youtube_metadata.md`.
- Proof status: oEmbed can lag (see `docs/youtube_oembed_delay_notes.md`). Fallback proofs live under `artifacts/video6/proof_fallback/`.

## In progress
- Video 7 draft is QC’d locally (proof bundles under `artifacts/video7/`) but not published yet.

## End screens (viewer flow)

Intended forward watch flow:
- Video 1 → Video 2
- Video 2 → Video 3
- Video 3 → Video 4

Proof (Video 3 end screen points to Video 4; Save is disabled/no unsaved changes):
- `artifacts/video3/proofs/video3_end_screen_points_to_video4_save_disabled_2026-05-19.png`
- `artifacts/video3/proofs/video3_end_screen_points_to_video4_save_disabled_2026-05-19_103940.png`

## Rendering slides
- Install dependencies (`pip install pillow pyyaml`).
- Run `python slides/render_slides.py` to read YAML (for example `slides/slide_text_video6.yaml`) and emit rendered PNGs.
- Renderer uses 1920×1080, dark background, teal titles, and DejaVu fonts when available.

## Licenses
- Code: MIT (see `LICENSE`)
- Content (script/slides/diagrams): CC BY 4.0 (see `CONTENT_LICENSE_CC_BY_4.0.txt`)

## Encoding note (YouTube processing reliability)
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
