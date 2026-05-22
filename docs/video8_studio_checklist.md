# Video 8 — YouTube Studio checklist (draft)

Video 8: **“Hard reload isn’t proof”**

Draft file to upload (gitignored):
- `build/video8/video8_upload_candidate_draft_loud.mp4`

QC references (committed):
- `artifacts/video8/qc/contact_sheet_midpoints.png`
- `artifacts/video8/qc/legibility_mosaic_320x180.png`

Local thumbnail drafts (committed):
- `artifacts/video8/thumbnail/thumbnail_v1.png`

Metadata draft (committed):
- `docs/video8_youtube_metadata.md`
- Chapters: `docs/video8_chapters_draft.md`

## Checklist

### Before upload
- [ ] Open QC images and do a quick scan for cropping/blur/wrong slide order.
- [ ] Confirm the file you’re uploading is the **loud** draft (`..._draft_loud.mp4`).

### Details
- [ ] Title matches `docs/video8_youtube_metadata.md`.
- [ ] Description pasted from `docs/video8_youtube_metadata.md`.
- [ ] Thumbnail: upload `artifacts/video8/thumbnail/thumbnail_v1.png` (or updated).
- [ ] Playlist: “Web Debugging Proofs (Cache & GitHub Pages)”
- [ ] Audience: **Not made for kids**.
- [ ] “Altered content” / synthetic disclosure: set appropriately (default: No, unless you add synthetic media).
- [ ] Category: Science & Technology.
- [ ] Tags set (optional): see `docs/video8_youtube_metadata.md`.

### More options / features
- [ ] Auto chapters: OFF (if you are providing custom chapters).
- [ ] Embedding: ON.
- [ ] Notify subscribers: OFF (if doing a quiet test upload).
- [ ] Remixing: choose intentionally (OK to disallow while Private).

### Visibility
- [ ] Set **Private** for initial upload review.
- [ ] After a final review, decide: Unlisted → Public.

### After publish (proof-first)
- [ ] Capture publish proof bundle:

```bash
python scripts/capture_youtube_publish_proof.py \
  --url "<youtube-watch-url>" \
  --out-dir artifacts/video8/publish_proof/<timestamp> \
  --include-body
```

Notes:
- The capture script uses `Accept-Encoding: identity` internally so responses stay inspectable.
- oEmbed can return HTTP 404 briefly after publish; retry later for `artifacts/video8/oembed.json`.
