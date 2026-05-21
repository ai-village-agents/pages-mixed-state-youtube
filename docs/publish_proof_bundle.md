## Publish Proof Bundle

We keep a lightweight bundle alongside uploads to show what was live on YouTube at upload time. The bundle normally contains:
- `oembed.json`: YouTube oEmbed JSON (only if the endpoint returns HTTP 200).
- `watch_headers.txt`: Status line and response headers from the watch page request (no gzip).
- `watch_body.html`: Raw watch page body (optional; enabled with `--include-body`).
- `SHA256SUMS.txt`: sha256 for every file above, sorted deterministically.

Capture a new bundle after publishing:

```sh
python scripts/capture_youtube_publish_proof.py \
  --url 'https://youtu.be/VIDEO_ID' \
  --out-dir artifacts/videoX/publish_proof \
  --include-body
```

Notes:
- It is possible for YouTube's oEmbed endpoint to temporarily return HTTP 404 for a newly published video.
  - In that case, the script will still write `watch_headers.txt` (and `watch_body.html` if requested), but it will **not** write `oembed.json`.
  - Re-run later; when oEmbed returns HTTP 200, `oembed.json` will be added and `SHA256SUMS.txt` will update accordingly.
  - You can also retry just oEmbed: `python scripts/fetch_youtube_oembed_json.py --url https://youtu.be/VIDEO_ID --out artifacts/videoX/publish_proof/oembed.json` (exits 3 and does not write unless HTTP 200).

You can pass `--user-agent` to override the default header if needed. Proof files write atomically, so partial outputs are avoided on errors.

## Local QC proof bundle

For local QC of drafts (without committing the MP4), capture ffmpeg inspection and loudness logs:

```sh
python scripts/capture_local_qc_proof.py \
  --in build/video7/video7_upload_candidate_draft_loud.mp4 \
  --out-dir artifacts/video7/local_qc_proof
```

This script stays local-only: it records `ffmpeg -i` stderr, a loudnorm snapshot, and hashes of the MP4 and bundle files, but does not commit the media. `scripts/capture_youtube_publish_proof.py` instead hits the YouTube endpoints after upload to document what was publicly served.
