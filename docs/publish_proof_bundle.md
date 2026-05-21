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

You can pass `--user-agent` to override the default header if needed. Proof files write atomically, so partial outputs are avoided on errors.
