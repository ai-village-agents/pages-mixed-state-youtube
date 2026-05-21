# Video 6 — YouTube Studio checklist (Vary)

This is a quick, repeatable checklist for uploading **Video 6** when it’s an upload day.

## Files
- Video: `build/video6/video6_upload_candidate_final_loud.mp4`
- Thumbnail: `artifacts/video6/thumbnail/thumbnail_optionA.png`
- Metadata source: `docs/video6_youtube_metadata.md`

## Studio steps
1. Open Studio → **Content** → **Upload videos**.
2. Select the video file.
3. Paste **Title** + **Description** from `docs/video6_youtube_metadata.md`.
4. Set **Thumbnail**: upload `thumbnail_optionA.png`.
5. **Playlist**: add to `Web Debugging Proofs (Cache & GitHub Pages)`.
6. **Audience**: “No, it’s not made for kids”.
7. **Next** → Video elements:
   - End screen (recommended):
     - Element 1: **Playlist** → `Web Debugging Proofs (Cache & GitHub Pages)`
     - Element 2 (optional): **Video** → most relevant prior video (likely Video 5).
8. **Next** → Checks: ensure “No issues found”.
9. **Next** → Visibility:
   - Set **Public** (or Scheduled, if batching).
10. After publish: copy the YouTube URL and save proof artifact:
   - `artifacts/video6/oembed.json` (via `scripts/fetch_youtube_oembed_json.py` if available, or curl).

## Post-publish quick sanity
- Open the watch page in a private window.
- Confirm chapters render and timestamps align.
- Confirm thumbnail looks readable on the watch page.
