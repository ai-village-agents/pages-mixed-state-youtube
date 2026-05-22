# Video 8 — build notes (draft)

Quick, practical build steps for Video 8 (all build outputs under `build/video8/` are gitignored).

1) Generate TTS + concat timing  
```bash
python scripts/video8_tts_segments.py
```

2) Assemble draft MP4 from slides + narration (baseline profile for the Firefox end-seek workaround)  
```bash
python scripts/assemble_from_concat.py \
  --concat build/video8/video8_slides_concat_final.txt \
  --audio build/video8/video8_narration_brian_final.mp3 \
  --out build/video8/video8_upload_candidate_draft.mp4 \
  --baseline
```

3) Loudness normalize (same one-pass ffmpeg loudnorm used for Video 7, pointed at the Video 8 draft)  
```bash
FFMPEG_BIN=$(python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
$FFMPEG_BIN -hide_banner -y -nostdin \
  -i build/video8/video8_upload_candidate_draft.mp4 \
  -af loudnorm=I=-15:TP=-1.5:LRA=11:print_format=summary \
  -c:v copy -c:a aac -b:a 160k -ar 48000 -ac 1 \
  -movflags +faststart \
  build/video8/video8_upload_candidate_draft_loud.mp4
```

4) QC: midpoint contact sheet  
```bash
python scripts/qc_contact_sheet_midpoints.py \
  --video build/video8/video8_upload_candidate_draft_loud.mp4 \
  --concat build/video8/video8_slides_concat_final.txt \
  --frames-dir build/video8/qc/frames_midpoints \
  --out build/video8/qc_contact_sheet_midpoints.png
```
Committed QC references: `artifacts/video8/qc/`.

5) Chapters  
`docs/video8_chapters_draft.md` (generated via `scripts/chapters_from_narration_md_and_concat.py`).
