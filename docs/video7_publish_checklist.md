# Video 7 — publish checklist

Publish once, capture proof, avoid churn: one clean upload to YouTube Studio, collect reproducible evidence immediately, and avoid edits that restart processing.

## 1) Pre-upload sanity (local)
1. Quick slide legibility scan at small size: open `artifacts/video7/qc/legibility_mosaic_320x180.png`.
2. Quick narrated-render visual scan: open `artifacts/video7/qc/contact_sheet_midpoints.png` (order/cropping/render glitches).
3. Confirm the final MP4 is the intended file (default: `build/video7/video7_upload_candidate_draft_loud.mp4`); double-check you did not pick an earlier draft.
4. Verify video codec/pixel format and audio codec: H.264 `yuv420p` + AAC (`ffprobe` or `scripts/capture_media_proof.py` output from the pre-publish proof bundle).
5. Confirm duration matches the expected slide timing; spot-check against `slides/rendered_video7/concat_timing_video7.txt` if you regenerated timing.
6. Loudness target: integrated loudness in **-14 to -16 LUFS** and true peak near **-1.5 dBTP** (per loudnorm summary). If out of range, rerun normalization before upload.

## 2) Metadata
1. Title: from `docs/video7_youtube_metadata.md`.
2. Description: paste the latest from `docs/video7_youtube_metadata.md`, including the proof checklist section and the repo artifact index link; include chapters if still valid.
3. Language: keep “service worker” phrasing cautious (say it **can intercept / can serve cached responses**; avoid implying it always runs or always causes the bug).
4. Add the short pinned-comment draft from `docs/video7_youtube_metadata.md` (keep it ready for the Comments tab after publish).

## 3) YouTube Studio steps
1. Upload the MP4.
2. Wait for “Checks” to finish; resolve blockers if any.
3. Set visibility to the intended state (typically Public on first publish); ensure the scheduled/published time is correct.
4. Add to playlist: `Web Debugging Proofs (Cache & GitHub Pages)`.
5. Add end screen: point to the prior video(s) in the series if appropriate; verify positioning.
6. Ensure the Save button is enabled, then click Save (no pending Studio edits).

## 4) Proof capture (immediate)
1. Immediately after publish, run `python scripts/capture_youtube_publish_proof.py --url "<video-url>" --out-dir artifacts/video7/publish_proof/<timestamp> --include-body`.
2. Script already uses `Accept-Encoding: identity` internally to avoid gzip/range artifacts.
3. Note: oEmbed may return 404 temporarily; retry later until it succeeds.
4. Store all outputs (HTML/JSON/screens, SHA256SUMS) under `artifacts/video7/publish_proof/` with timestamped subfolders.
5. Pre-publish proof for this render lives at `artifacts/video7/proof_draft_loud_v3/`.

## 5) Post-publish QA
1. Open the watch page in a private window to avoid stale service-worker/browser state.
2. Confirm chapters render correctly on the seek bar (or remove from description if they do not match).
3. Confirm description links, especially the artifact index/proof checklist links, resolve as expected.
4. Play a few loud passages to confirm no obvious clipping or distortion.
