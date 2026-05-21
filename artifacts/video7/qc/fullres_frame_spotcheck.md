# Video 7 — Full-resolution frame spot-check (draft)

Purpose: a quick sanity-check that slide text remains sharp/legible in the **1920×1080** encoded draft MP4 (not just in 320×180 thumbnails).

Input:
- `build/video7/video7_upload_candidate_draft_loud.mp4` (gitignored)

Method:
- Extract a small set of 1080p frames at fixed timestamps using `ffmpeg` (via the `imageio_ffmpeg` fallback binary) and inspect visually.

Commands used:
```bash
cd /home/computeruse/pages-mixed-state-youtube
ff="$(python -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')"
mkdir -p /tmp/video7_frames_fullres

# Extract a few frames (seconds into the MP4)
for ts in 5 30 60 100 150; do
  "$ff" -nostdin -hide_banner -loglevel error -y \
    -ss "$ts" -i build/video7/video7_upload_candidate_draft_loud.mp4 \
    -frames:v 1 \
    "/tmp/video7_frames_fullres/frame_${ts}s.png"
done

sha256sum /tmp/video7_frames_fullres/frame_*s.png
```

Frames extracted:
- `/tmp/video7_frames_fullres/frame_5s.png` (title slide)
- `/tmp/video7_frames_fullres/frame_30s.png` (slide 3)
- `/tmp/video7_frames_fullres/frame_60s.png` (slide 5)
- `/tmp/video7_frames_fullres/frame_100s.png` (slide 7)
- `/tmp/video7_frames_fullres/frame_150s.png` (slide 10)

Notes:
- This spot-check is **not** a substitute for mobile playback testing; it’s only a quick visual confirmation that the encoded frames don’t look unexpectedly soft.
- The extracted frames are in `/tmp` and are not committed.
