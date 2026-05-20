# Video 7 — Service Worker (work in progress)

This folder contains lightweight, tracked artifacts for Video 7.

## Thumbnail
- `thumbnail/thumbnail_optionA.png` — 1280×720 thumbnail candidate based on Slide 1.
- `thumbnail/thumbnail_optionA_preview_640x360.png`, `thumbnail/thumbnail_optionA_preview_320x180.png` — downscaled previews for readability checks.

## QC
- `qc/contact_sheet_midpoints.png` — a 10-frame contact sheet taken at the midpoint of each slide segment, generated from `build/video7/video7_slides_concat_final.txt`.
  - Purpose: quick visual scan for slide order, cropping, and obvious rendering glitches.

> Note: intermediate build outputs (audio/video candidates, per-slide frames, etc.) live under `build/` and are gitignored.
