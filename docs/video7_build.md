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

## Planned steps (high level)
1. Lock slide copy + order.
2. Generate narration (per-slide segments):

```bash
python scripts/video7_tts_segments.py
```
3. Assemble video from slides (per-slide durations) + narration.
4. Loudness normalize to ~-15 LUFS integrated.
5. QC:
   - midpoint contact sheet
   - listen for pops/clicks and pacing issues
6. Prepare thumbnail.
7. Upload using a Studio checklist; save oEmbed proof after publish.
