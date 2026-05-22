# Video 7 — build notes (draft)

This is a **draft** build checklist for Video 7.

## Inputs
- Slide text: `slides/slide_text_video7.yaml`
- Rendered slides: `slides/rendered_video7/slide_*.png`

## Output targets (YouTube-safe defaults)
- H.264 + AAC, `yuv420p`
- CFR 30 fps
- `-movflags +faststart`
- Add `-nostdin` to ffmpeg calls

## Step-by-step (draft build)

### 0) Render slides (if needed)

Video 7 slides currently use larger font overrides for legibility at 320x180 preview sizes.

```bash
python slides/render_slides.py \
  --input slides/slide_text_video7.yaml \
  --output-dir slides/rendered_video7 \
  --title-size 72 --body-size 44 --code-size 36 --note-size 30 --footer-size 28

# Optional: montage (slides only; exclude preview PNGs)
python slides/make_montage.py slides/rendered_video7 \
  --pattern "slide_[0-9][0-9].png" \
  --out slides/rendered_video7/_montage.png

# Optional: regenerate previews for slide_XX.png and _montage.png
python slides/make_previews.py --sizes 320x180,640x360 slides/rendered_video7/slide_[0-9][0-9].png
python slides/make_previews.py --sizes 320x180,640x360 slides/rendered_video7/_montage.png

# QC: legibility mosaic
python scripts/make_legibility_mosaic.py
```

### 1) Generate narration (per-slide segments)

```bash
python scripts/video7_tts_segments.py --force
```

This writes (gitignored):
- `build/video7/video7_narration_brian_final.mp3`
- `build/video7/video7_slides_concat_final.txt`

Notes:
- If you edit `script/VIDEO7_narration.md`, re-run with `--force` (or let the hash manifest invalidate stale slide segments).
- The concat list includes a **final repeated** `file ... slide_10.png` line. This is intentional for ffmpeg concat-demuxer timing semantics so the previous `duration` applies to the last real frame.

### 2) Assemble draft MP4 from slides + narration

```bash
python scripts/assemble_from_concat.py \
  --concat build/video7/video7_slides_concat_final.txt \
  --audio build/video7/video7_narration_brian_final.mp3 \
  --out build/video7/video7_upload_candidate_draft.mp4 \
  --baseline
```

The `--baseline` flag encodes the final output as H.264 **Constrained Baseline** + AAC 48k + faststart (a workaround for a Firefox end-seek anomaly seen in earlier videos).

### 3) Loudness normalize (draft)

One-pass loudness normalization (good enough for a draft):

```bash
FFMPEG_BIN=$(python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
$FFMPEG_BIN -hide_banner -y -nostdin \
  -i build/video7/video7_upload_candidate_draft.mp4 \
  -af loudnorm=I=-15:TP=-1.5:LRA=11:print_format=summary \
  -c:v copy -c:a aac -b:a 160k -ar 48000 -ac 1 \
  -movflags +faststart \
  build/video7/video7_upload_candidate_draft_loud.mp4
```

Draft loudnorm summary (from a sample run):
- Input integrated: **-20.7 LUFS**
- Output integrated: **-15.7 LUFS**
- Output true peak: **-1.5 dBTP**

### 4) Generate chapters (optional)

```bash
python scripts/chapters_from_narration_md_and_concat.py \
  --narration-md script/VIDEO7_narration.md \
  --concat build/video7/video7_slides_concat_final.txt \
  --mode round
```

(Use `--mode floor` if you prefer strictly-not-after boundaries.)

### 5) QC — midpoint contact sheet

```bash
python scripts/qc_contact_sheet_midpoints.py \
  --video build/video7/video7_upload_candidate_draft_loud.mp4 \
  --concat build/video7/video7_slides_concat_final.txt \
  --frames-dir build/video7/qc/frames_midpoints \
  --out build/video7/qc_contact_sheet_midpoints.png
```

Tracked artifact (committed):
- `artifacts/video7/qc/contact_sheet_midpoints.png`

### 6) Upload checklist + proof
- Use a Studio checklist (draft): `docs/video7_upload_plan.md`.
- After publish, capture proof (proof-first):

```bash
python scripts/capture_youtube_publish_proof.py \
  --url "<youtube-watch-url>" \
  --out-dir artifacts/video7/publish_proof/<timestamp> \
  --include-body
```

- The capture script sends `Accept-Encoding: identity` internally so responses stay inspectable.
- oEmbed can 404 briefly after publish; retry later (re-run the capture script or use `scripts/fetch_youtube_oembed_json.py` directly).

## Slides concat (sanitized timing)

Recommended committed timing file (no absolute paths):
- `slides/rendered_video7/concat_timing_video7.txt`

### Option A: ffmpeg directly

```bash
cd slides/rendered_video7
ffmpeg -nostdin -y -f concat -safe 0 -i concat_timing_video7.txt   -r 30 -pix_fmt yuv420p -vcodec libx264 /tmp/video7_slides.mp4
```

### Option B: helper script

```bash
python scripts/render_slides_from_concat_timing.py   --timing-file slides/rendered_video7/concat_timing_video7.txt   --slides-dir slides/rendered_video7   --out /tmp/video7_slides.mp4
```

Then merge `/tmp/video7_slides.mp4` with your narration audio as usual.

## Proof artifacts (recommended)
To create commit-friendly proof artifacts for a built MP4 without committing the MP4 itself:

```bash
python scripts/capture_local_qc_proof.py \
  --in build/video7/video7_upload_candidate_draft_loud.mp4 \
  --out-dir artifacts/video7/proof_draft_loud_v4/<timestamp>/
```
This writes `ffmpeg -i` output, loudnorm analysis JSON, and `SHA256SUMS.txt` (including the local MP4 hash) to the chosen folder.

Example (latest bundle as of 2026-05-22): `artifacts/video7/proof_draft_loud_v4/20260522T172533Z/`.
