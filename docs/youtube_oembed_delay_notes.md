# Notes: YouTube oEmbed can lag behind publish (HTTP 404)

This repo’s proof-first workflow prefers capturing YouTube’s **oEmbed JSON** (when available) as a compact, machine-readable “published video exists” proof.

However, we’ve observed that **newly published videos may temporarily return HTTP 404 from the YouTube oEmbed endpoint** even while:
- the watch page loads (HTTP 200), and
- the embed page loads (HTTP 200).

This appears to be a **propagation/availability delay** (or other transient condition) on YouTube’s side. The main practical implication for this repo:

- **Do not write `artifacts/*/oembed.json` until oEmbed returns HTTP 200.**
- While waiting, capture “fallback” proofs (watch headers/body) with `Accept-Encoding: identity` and deterministic SHA256 sums.

## Quick check (non-writing)

This exits 0 only when oEmbed is HTTP 200:

```bash
python scripts/check_youtube_oembed_status.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
```
The scripts default to a `curl` backend with strict timeouts to avoid hangs; `--backend python` exists as a fallback.

```bash
python scripts/check_youtube_oembed_status.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --backend curl --timeout 20 --connect-timeout 5
```

Example (Video 6, as observed on Day 415):

```bash
python scripts/check_youtube_oembed_status.py --url "https://www.youtube.com/watch?v=KZEPlZKGq7A"
# 404 ... (reason: Not Found)
```

## When it flips to HTTP 200 (write the proof JSON)

Only after the check returns HTTP 200, fetch and write the oEmbed JSON:

```bash
python scripts/fetch_youtube_oembed_json.py \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --out "artifacts/<videoN>/oembed.json"
```

That script:
- forces `Accept-Encoding: identity` to avoid gzip/range confusion,
- writes atomically, and
- refuses to write if the HTTP status is not 200.

## Fallback proof bundle (when oEmbed is not ready)

Use `scripts/capture_youtube_publish_proof.py` to capture watch headers/body and (if available) oEmbed, plus deterministic sums.

See:
- `docs/publish_proof_bundle.md`

