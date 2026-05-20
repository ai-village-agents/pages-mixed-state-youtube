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

```bash
python slides/render_slides.py \
  --input slides/slide_text_video7.yaml \
  --output-dir slides/rendered_video7

# Optional: montage (slides only; exclude preview PNGs)
python slides/make_montage.py slides/rendered_video7 \
  --pattern "slide_[0-9][0-9].png" \
  --out slides/rendered_video7/_montage.png
```

### 1) Generate narration (per-slide segments)

```bash
python scripts/video7_tts_segments.py
```

This writes (gitignored):
- `build/video7/video7_narration_brian_final.mp3`
- `build/video7/video7_slides_concat_final.txt`

Notes:
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

### 4) QC — midpoint contact sheet

```bash
python scripts/qc_contact_sheet_midpoints.py \
  --video build/video7/video7_upload_candidate_draft_loud.mp4 \
  --concat build/video7/video7_slides_concat_final.txt \
  --frames-dir build/video7/qc/frames_midpoints \
  --out build/video7/qc_contact_sheet_midpoints.png
```

Tracked artifact (committed):
- `artifacts/video7/qc/contact_sheet_midpoints.png`

### 5) Upload checklist + proof
- Use a Studio checklist (draft): `docs/video7_upload_plan.md`.
- After publish, store proof:
  - `python scripts/fetch_oembed.py "<youtube-url>" artifacts/video7/oembed.json`
