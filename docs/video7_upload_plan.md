# Video 7 — upload plan

Status: **draft narrated export exists (local)** + **QC proof bundle captured**. Not uploaded yet.

Current local draft (audio loudnorm applied):
- `build/video7/video7_upload_candidate_draft_loud.mp4`

Most recent local QC proof bundle:
- `artifacts/video7/proof_draft_loud_v4/20260522T172533Z/`

## Target timing
- Keep channel rule: **max 1 upload/day**.

## Pre-upload checklist (local)
- Re-watch the draft for:
  - slide legibility at 320×180 thumbnail scale
  - any timing/rhythm problems between slide transitions
  - audio: no clipping, no audible glitches
- Confirm the 320×180 legibility mosaic is current:
  - `python scripts/make_legibility_mosaic.py`
  - output: `artifacts/video7/qc/legibility_mosaic_320x180.png`
- Confirm a midpoint contact sheet exists for timing/transition sanity:
  - `artifacts/video7/qc/contact_sheet_midpoints.png`
- Optional: spot-check a few full-res (1080p) frames using:
  - `artifacts/video7/qc/fullres_frame_spotcheck.md`

If a new draft/final MP4 is rendered, capture an updated local QC proof bundle:

```sh
python scripts/capture_local_qc_proof.py \
  --in build/video7/<mp4> \
  --out-dir artifacts/video7/proof_<...>/<timestamp>/
```

## Upload + publish-proof plan
1. Upload to YouTube.
2. After publish, capture a publish-proof bundle (oEmbed + watch headers/body + deterministic SHA256SUMS):

```sh
python scripts/capture_youtube_publish_proof.py \
  --url <video-url> \
  --out-dir artifacts/video7/publish_proof/<timestamp>/ \
  --include-body
```

If oEmbed returns HTTP 404 temporarily, follow:
- `docs/youtube_oembed_delay_notes.md`

## Thumbnail
- Upload: `artifacts/video7/thumbnail/thumbnail_optionA.png`
- Small-size check: `artifacts/video7/thumbnail/thumbnail_optionA_preview_320x180.png`
