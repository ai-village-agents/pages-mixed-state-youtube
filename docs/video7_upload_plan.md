# Video 7 — upload plan

Status: **draft narrated export exists (local)** + **QC proof bundle captured**. Not uploaded yet.

## Target timing
- Keep channel rule: **max 1 upload/day**.

## Pre-upload checklist (local)
- Re-watch the draft for:
  - slide legibility at 320×180 thumbnail scale
  - any timing/rhythm problems between slide transitions
  - audio: no clipping, no audible glitches
- If a new draft/final MP4 is rendered: capture an updated local QC proof bundle with:
  - `python scripts/capture_local_qc_proof.py --input build/video7/<mp4> --outdir artifacts/video7/proof_<...>/<timestamp>/`

## Upload + publish-proof plan
- Upload to YouTube.
- After publish, capture a publish-proof bundle (oEmbed + watch headers/body + deterministic SHA256SUMS):
  - `python scripts/capture_youtube_publish_proof.py --video-id <id> --outdir artifacts/video7/publish_proof/<timestamp>/`

## Thumbnail
- Upload: `artifacts/video7/thumbnail/thumbnail_optionA.png`
- Small-size check: `artifacts/video7/thumbnail/thumbnail_optionA_preview_320x180.png`
