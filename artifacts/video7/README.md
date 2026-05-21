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
As of 2026-05-20, a draft narrated build was generated locally (not committed):
- `build/video7/video7_upload_candidate_draft.mp4`
- `build/video7/video7_upload_candidate_draft_loud.mp4` (one-pass loudnorm)

### Local QC proof bundle (tracked)

Recommended proof format (captures the local MP4 hash in `SHA256SUMS.txt`):
- `proof_draft_loud_v3/20260521T190000Z/`
  - `ffmpeg_i.txt` — `ffmpeg -i` stream summary (stderr capture).
  - `loudnorm_analysis.json` — loudnorm analysis JSON.
  - `loudnorm_pass_log.txt` — loudnorm pass log.
  - `SHA256SUMS.txt` — hashes of the tracked proof artifacts **and the local MP4**.
  - `README.md` — short, human-readable snapshot.

Loudness snapshot (from the v3 bundle):
- `input_i`: **-15.72 LUFS**
- `output_i`: **-15.28 LUFS**
- `output_tp`: **-1.50 dBTP**
- `output_lra`: **2.00 LU**

Convenience (non-timestamped) copies also exist under `proof_draft_loud_v3/`.

Earlier captures (still valid):
- `proof_draft_loud_v2/` (non-timestamped proof artifacts + sums)
- `proof_draft/` (legacy proof format)

Build notes / reproduction: `docs/video7_build.md`.

## Slides-only proof (tracked)
- `proof_slides_only/ffmpeg_i_video7_slides_only.mp4.txt` — `ffmpeg -i` summary for the slides-only render from sanitized timing.
- `proof_slides_only/loudnorm_analysis_video7_slides_only.mp4.json` — loudnorm analysis JSON.
- `proof_slides_only/SHA256SUMS.txt` — hashes covering the above and the slides-only MP4.
- MP4 itself: `build/video7/video7_slides_only.mp4` (local, gitignored).

## Reproducibility

- Sanitized slide concat timing (no absolute paths): `slides/rendered_video7/concat_timing_video7.txt`
  - Usage: `cd slides/rendered_video7 && ffmpeg -nostdin -y -f concat -safe 0 -i concat_timing_video7.txt -r 30 -pix_fmt yuv420p -vcodec libx264 /tmp/video7_slides.mp4` (example)
