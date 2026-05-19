# Video 5 build notes (reproducible)

This repo keeps **source** (scripts + slide YAML + renderers) under version control, but keeps **renders** in `build/` (gitignored). These notes document a reproducible, copy/paste pipeline for assembling **Video 5**.

## 0) Prereqs

- Python 3
- A working ffmpeg binary. This environment does not always have `ffmpeg` on `PATH`, so we use the copy shipped with `imageio-ffmpeg`.

Locate ffmpeg:

```bash
python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"
```

(If needed: `pip install imageio-ffmpeg`.)

## 1) Render slides

Video 5 slide spec:
- `slides/slide_text_video5.yaml`

Render:

```bash
python slides/render_slides.py \
  --input slides/slide_text_video5.yaml \
  --output-dir slides/rendered_video5
```

Tip: YAML values that contain header-like strings **must be quoted**, e.g.

```yaml
- "Cache-Control: max-age=60"
- "ETag: \"abc\""
```

## 2) Prepare a concat list (timed still frames)

We assemble the video from still PNGs with per-slide durations using ffmpeg’s **concat demuxer**.

Create a file like `build/video5_slides_concat.txt`:

```text
file '/abs/path/to/slides/rendered_video5/slide_01.png'
duration 21.50
file '/abs/path/to/slides/rendered_video5/slide_02.png'
duration 51.19
...
file '/abs/path/to/slides/rendered_video5/slide_10.png'
duration 36.04
# IMPORTANT: repeat the last file with no duration line (ffmpeg concat demuxer rule)
file '/abs/path/to/slides/rendered_video5/slide_10.png'
```

Notes:
- Prefer **absolute paths** in the concat file.
- Use `-safe 0` when consuming it.

## 3) Prepare narration audio

The current pipeline expects an audio file (for Video 5 we used an MP3).

Example (edge-tts via module; CLI may not be on PATH):

```bash
python -m edge_tts \
  --voice en-US-BrianNeural \
  --file build/video5_narration.txt \
  --write-media build/video5_narration.mp3 \
  --write-subtitles build/video5_narration.vtt
```

## 4) Assemble (important pitfalls + known-good workflow)

### Pitfall: don’t force CFR during concat

Forcing constant frame rate **during the concat step** (e.g. `-vf fps=30` or `-r 30` while reading the concat list) can cause **mass frame duplication** and **duration inflation**.

**Known-good workflow:**

1) concat → **VFR** intermediate
2) VFR → **CFR 30** intermediate
3) mux narration

### Firefox end-seek “file is corrupt” symptom

Some encodes will play from the start in Firefox but fail when seeking to the end (timeline click or End key) with an overlay like:

> “Video can’t be played because the file is corrupt.”

Workaround that has been stable here:
- Re-encode final output as **H.264 Constrained Baseline** + **AAC 48 kHz** + `-movflags +faststart`.

## 5) One-command helper

Use the helper script:

```bash
python scripts/assemble_from_concat.py \
  --concat build/video5_slides_concat.txt \
  --audio build/video5_narration.mp3 \
  --out build/video5_upload_candidate.mp4 \
  --baseline
```

It will produce intermediates under a temporary directory and then a final MP4 at `--out`.

Dry run:

```bash
python scripts/assemble_from_concat.py --concat build/video5_slides_concat.txt --audio build/video5_narration.mp3 --out build/out.mp4 --baseline --dry-run
```

## 6) Quick QC checks

Loudness summary (targeting ~-14 LUFS):

```bash
FFMPEG=$(python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
"$FFMPEG" -hide_banner -nostdin -i build/video5_upload_candidate.mp4 \
  -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=summary \
  -f null -
```

Measure loudness *as-is* (no output file; prints analysis JSON):

```bash
FFMPEG=$(python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
"$FFMPEG" -hide_banner -nostdin -i build/video5_upload_candidate.mp4 \
  -af loudnorm=print_format=json \
  -f null -
"$FFMPEG" -hide_banner -nostdin -i build/video5_upload_candidate_loud.mp4 \
  -af loudnorm=print_format=json \
  -f null -
```

Recorded measurements in this environment (from `input_i` / `input_tp`):
- `build/video5_upload_candidate.mp4`: ~**-20.4 LUFS**, ~**-2.7 dBTP** (too quiet)
- `build/video5_upload_candidate_loud.mp4`: ~**-15.1 LUFS**, ~**-1.4 dBTP**

**Chosen upload artifact:** `build/video5_upload_candidate_loud.mp4`

How the louder variant was produced (copy video, normalize audio, keep faststart):

```bash
FFMPEG=$(python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
"$FFMPEG" -hide_banner -nostdin -i build/video5_upload_candidate.mp4 \
  -c:v copy \
  -c:a aac -b:a 192k -ar 48000 \
  -af loudnorm=I=-14:TP=-1.5:LRA=11 \
  -movflags +faststart \
  build/video5_upload_candidate_loud.mp4
```

Firefox seek check:
- Open `file:///.../build/video5_upload_candidate.mp4`
- Press **End** and scrub near the end; confirm no “corrupt” overlay.
