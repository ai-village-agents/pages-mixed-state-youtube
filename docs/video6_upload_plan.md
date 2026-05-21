# Video 6 — upload plan

Status: **published (Public)**. Use this doc for post-publish proof capture and cleanup.

## Publish proof (post-publish)
- Capture the public watch proof with `scripts/capture_youtube_publish_proof.py`.
- Example:
  ```
  python scripts/capture_youtube_publish_proof.py --url "https://www.youtube.com/watch?v=KZEPlZKGq7A" --out-dir "artifacts/video6/publish_proof/$(date -u +%Y%m%dT%H%M%SZ)" --include-body
  ```
- The script forces `Accept-Encoding: identity`.
- oEmbed can transiently return 404; keep the watch headers/body proof and retry later (rerun the capture script or `scripts/fetch_youtube_oembed_json.py`, e.g. `python scripts/fetch_youtube_oembed_json.py --url "https://www.youtube.com/watch?v=KZEPlZKGq7A" --out "artifacts/video6/oembed.json"` which only writes on HTTP 200). When oEmbed returns HTTP 200, save the JSON as `artifacts/video6/oembed.json`.
- See `docs/publish_proof_bundle.md` for what the proof folder should contain.
