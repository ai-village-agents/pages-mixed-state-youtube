# Video 7 — QC artifacts (draft)

This folder contains **QC artifacts** for Video 7 (draft build).

## Contact sheet
- `contact_sheet_midpoints.png`
  - A grid of midpoint frames (one per slide), extracted from a draft narrated MP4.

## Legibility (320×180)
- `legibility_mosaic_320x180.png`
  - A 5×2 mosaic of the slide previews at **exactly 320×180** each (i.e., “small thumbnail” scale).
  - Generated from `slides/rendered_video7/slide_??_preview_320x180.png` (not from the narrated MP4).
  - Purpose: quick check that headers and bullet text remain readable at small sizes.

## Slide timing (from generated concat list)
Total slide time (padded): **165.39s**.

| Slide | Duration (s) |
|------:|-------------:|
| 01 | 13.060 |
| 02 | 12.460 |
| 03 | 14.090 |
| 04 | 12.800 |
| 05 | 30.150 |
| 06 | 13.450 |
| 07 | 18.080 |
| 08 | 12.940 |
| 09 | 22.900 |
| 10 | 15.460 |

## Draft build notes

- For a timestamped, reproducible *local QC proof bundle* (ffmpeg inspection + loudnorm analysis/log + SHA256SUMS including the local MP4 hash), see:
  - `artifacts/video7/proof_draft_loud_v3/20260521T190000Z/`
- Draft MP4 duration observed: ~**02:43.92**.
- Draft narration loudness (single-pass `loudnorm`) summary:
  - Input integrated: **-20.7 LUFS**
  - Output integrated: **-15.7 LUFS**
  - Output true peak: **-1.5 dBTP**

(Inputs/outputs live under `build/video7/` and are gitignored.)
