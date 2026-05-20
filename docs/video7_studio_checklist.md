# Video 7 — Studio checklist (draft)

This is a **draft** checklist for uploading Video 7.

## Before you open Studio
- Confirm thumbnail readability (small size):
  - `artifacts/video7/thumbnail/thumbnail_optionA_preview_320x180.png`
- Confirm slide order / obvious glitches:
  - `artifacts/video7/qc/contact_sheet_midpoints.png`

## In YouTube Studio (Video details)
1. Upload the MP4 (gitignored local build output, path may change):
   - `build/video7/video7_upload_candidate_draft_loud.mp4`
2. Title: see `docs/video7_youtube_metadata.md`.
3. Description: paste from `docs/video7_youtube_metadata.md`.
4. Thumbnail: upload `artifacts/video7/thumbnail/thumbnail_optionA.png`.
5. Playlist:
   - `Web Debugging Proofs (Cache & GitHub Pages)`
6. Audience: **No, it’s not made for kids**.

## Checks / polish
- Add chapters (draft list in `docs/video7_youtube_metadata.md`).
- Add end screen + cards (targeting latest videos in the series).
- Preview the watch page on desktop + small player; confirm slide text is readable.

## After publish
- Save proof:
  - `python scripts/fetch_oembed.py "<youtube-url>" artifacts/video7/oembed.json`
