# Video 7 — Service Worker (work in progress)

This folder contains lightweight, tracked artifacts for Video 7.

## Thumbnail
- `thumbnail/thumbnail_optionA.png` — 1280×720 thumbnail candidate based on Slide 1.
- `thumbnail/thumbnail_optionA_preview_640x360.png`, `thumbnail/thumbnail_optionA_preview_320x180.png` — downscaled previews for readability checks.

## QC
- `qc/contact_sheet_midpoints.png` — a 10-frame contact sheet taken at the midpoint of each slide segment, generated from `build/video7/video7_slides_concat_final.txt`.
  - Purpose: quick visual scan for slide order, cropping, and obvious rendering glitches.

> Note: intermediate build outputs (audio/video candidates, per-slide frames, etc.) live under `build/` and are gitignored.

## Draft build (local, gitignored)
As of 2026-05-20, a draft build was generated locally (not committed):
- `build/video7/video7_upload_candidate_draft.mp4`
- `build/video7/video7_upload_candidate_draft_loud.mp4` (one-pass loudnorm)

Tracked *proof-of-build* artifacts:
- `proof_draft/ffmpeg_i_video7_upload_candidate_draft_loud.txt` — `ffmpeg -i` stream summary.
- `proof_draft/loudnorm_analysis_video7_upload_candidate_draft_loud.json` — loudnorm analysis (`I=-15, TP=-1.5, LRA=11`).
- `proof_draft/SHA256SUMS.txt` — hashes of the tracked proof artifacts.

Build notes / reproduction: `docs/video7_build.md`.

## Slides-only proof (tracked)
- `proof_slides_only/ffmpeg_i_video7_slides_only.mp4.txt` — `ffmpeg -i` summary for the slides-only render from sanitized timing.
- `proof_slides_only/loudnorm_analysis_video7_slides_only.mp4.json` — loudnorm analysis JSON.
- `proof_slides_only/SHA256SUMS.txt` — hashes covering the above and the slides-only MP4.
- MP4 itself: `build/video7/video7_slides_only.mp4` (local, gitignored).

## Reproducibility

- Sanitized slide concat timing (no absolute paths): `slides/rendered_video7/concat_timing_video7.txt`
  - Usage: `cd slides/rendered_video7 && ffmpeg -nostdin -y -f concat -safe 0 -i concat_timing_video7.txt -r 30 -pix_fmt yuv420p -vcodec libx264 /tmp/video7_slides.mp4` (example)
