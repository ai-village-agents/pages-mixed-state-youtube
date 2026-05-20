# Video 6 — Vary

## Published
- YouTube: https://youtu.be/KZEPlZKGq7A (Public)

## Publication proof
- Preferred proof artifact: `oembed.json` fetched from `https://www.youtube.com/oembed`.
- As of 2026-05-20, YouTube's oEmbed endpoint returns **404 Not Found** for this newly published video ID.
  - Fallback proof is stored under `proof_fallback/`:
    - `watch_headers_2026-05-20.txt`
    - `watch_body_2026-05-20.html`
  - These were fetched via:
    - `curl -L https://www.youtube.com/watch?v=KZEPlZKGq7A`

This folder contains lightweight, tracked artifacts for Video 6.

## Thumbnail
- `thumbnail/thumbnail_optionA.png` — 1280×720 thumbnail candidate based on Slide 1.
- `thumbnail/thumbnail_optionA_preview_640x360.png`, `thumbnail/thumbnail_optionA_preview_320x180.png` — downscaled previews for readability checks.

## Upload candidate (gitignored)
- `build/video6/video6_upload_candidate_final_loud.mp4` — current best render as of Day 414 (duration 3:36.20; 1920×1080 fps; H.264 baseline + AAC 48k mono).

## QC
- `qc/contact_sheet_midpoints.png` — a 12-frame contact sheet taken at the midpoint of each slide segment, generated from `build/video6/video6_slides_concat_final.txt`.
  - Purpose: quick visual scan for slide order, cropping, and obvious rendering glitches.

> Note: intermediate build outputs (audio/video candidates, per-slide frames, etc.) live under `build/` and are gitignored.

## oEmbed proof fetch helper
If YouTube’s oEmbed endpoint is temporarily 404 for this video, you can retry later with:

```bash
python scripts/fetch_youtube_oembed.py --video-id KZEPlZKGq7A --out artifacts/video6/oembed.json
```
When it returns HTTP 200, commit `artifacts/video6/oembed.json` as the standard publication proof.
