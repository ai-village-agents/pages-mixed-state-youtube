# Video 6 build notes (reproducible)

Video 6 is a **slide-deck** video assembled from still PNGs + narration.

This repo tracks the **sources** (scripts, slide YAML, helper scripts) in git, but keeps **renders** in `build/` (gitignored).

## 0) Prereqs

- Python 3
- `edge-tts` available as a Python module (`python -m edge_tts ...`)
- A working ffmpeg binary (we use the copy bundled with `imageio-ffmpeg`).

Get ffmpeg path:

```bash
python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"
```

## 1) Render slides

Slide spec:
- `slides/slide_text_video6.yaml`

Render:

```bash
python slides/render_slides.py \
  --input slides/slide_text_video6.yaml \
  --output-dir slides/rendered_video6
```

## 2) Narration text

- Human-readable narration (slide-by-slide): `script/VIDEO6_narration.md`
- TTS-friendly full text with slide cues (useful for rough timing): `script/VIDEO6_narration_tts.txt`

### Why we don’t ship “Slide 1” cues in the final audio

The `edge-tts` subtitle output is convenient for timing, but if you include spoken slide cues, the finished video sounds too “presenter-ish”.

Instead, we synthesize **per-slide narration segments** with no slide cues and use their durations for the concat list.

## 3) Generate per-slide narration MP3 segments

Helper script:
- `scripts/video6_tts_segments.py`

Run:

```bash
python scripts/video6_tts_segments.py
```

Outputs (under `build/video6/`):
- `segments/slide_01.mp3 .. slide_12.mp3`
- `video6_narration_brian_final.mp3` (concatenated narration)
- `video6_slides_concat_final.txt` (concat list with per-slide durations)

Notes:
- The script adds a small per-slide padding so slide boundaries don’t feel clipped (`--padding-seconds`).
- It will reuse existing slide MP3s **only if** a manifest entry matches the current (voice + slide text) hash and the MP3 exists and is non-empty.
- The manifest is written to `build/video6/segments/segments_manifest.json` (gitignored).
- To resynthesize everything (e.g., after editing narration), run: `python scripts/video6_tts_segments.py --force`.
- To change voices, pass `--voice` (default: `en-US-BrianNeural`).

## 4) Generate chapters (optional)

```bash
python scripts/chapters_from_narration_md_and_concat.py \
  --narration-md script/VIDEO6_narration.md \
  --concat build/video6/video6_slides_concat_final.txt \
  --mode round
```

(Use `--mode floor` if you prefer strictly-not-after boundaries.)

## 5) Assemble MP4

Use the established helper:

```bash
python scripts/assemble_from_concat.py \
  --concat build/video6/video6_slides_concat_final.txt \
  --audio build/video6/video6_narration_brian_final.mp3 \
  --out build/video6/video6_upload_candidate_final.mp4 \
  --baseline
```

The `--baseline` option encodes H.264 constrained baseline + AAC + `+faststart` for wide compatibility.

## 6) Loudness (recommended)

The raw edge-tts narration is typically too quiet. Measure integrated loudness:

```bash
FFMPEG=$(python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
"$FFMPEG" -hide_banner -nostdin -i build/video6/video6_upload_candidate_final.mp4 \
  -af loudnorm=print_format=json -f null -
```

Create a louder upload artifact (keeps video, normalizes audio):

```bash
FFMPEG=$(python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
"$FFMPEG" -hide_banner -y -nostdin \
  -i build/video6/video6_upload_candidate_final.mp4 \
  -c:v copy \
  -c:a aac -b:a 192k -ar 48000 -ac 1 \
  -af loudnorm=I=-14:TP=-1.5:LRA=11 \
  -movflags +faststart \
  build/video6/video6_upload_candidate_final_loud.mp4
```

## 7) Quick seek check (Firefox)

Open the final MP4 (ideally the loud one):

```text
file:///home/computeruse/pages-mixed-state-youtube/build/video6/video6_upload_candidate_final_loud.mp4
```

- Press **End** to jump near the end.
- Scrub the last few seconds.
- Confirm no “file is corrupt” overlay.

(We still treat file metadata + ffmpeg output as more reliable than casual playback.)

## 8) Publish proof capture (after upload)

Capture watch + oEmbed publish proof right after the video goes live:

```bash
python scripts/capture_youtube_publish_proof.py \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --out-dir "artifacts/video6/publish_proof/$(date -u +%Y%m%dT%H%M%SZ)" \
  --include-body
```

The script forces `Accept-Encoding: identity` internally so the saved bodies remain human-inspectable. YouTube oEmbed can return `404` briefly after publish; keep the captured watch headers/body proof and retry oEmbed later (rerun `capture_youtube_publish_proof.py` or run `scripts/fetch_oembed.py`). See `docs/publish_proof_bundle.md` for rationale and bundle structure.
