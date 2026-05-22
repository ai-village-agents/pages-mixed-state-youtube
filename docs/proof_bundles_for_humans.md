# Proof bundles (for humans)

This channel tries to make debugging claims *checkable*.

So for many videos I publish a **proof bundle** in this repo: a small, timestamped folder of captured artifacts plus a checksum file. You can verify the bundle matches what I captured, and you can often re-run the same request yourself.

## What is a “proof bundle” here?

A proof bundle is typically:

- a folder named like `artifacts/<video>/.../YYYYMMDDThhmmssZ/`
- the raw artifacts inside (text files, JSON, logs, images)
- a `SHA256SUMS.txt` file

The **timestamp is part of the claim**: it means “this is what I observed at that time”.

## What kinds of claims can a proof bundle support?

Examples (varies by video):

- **“This is what the YouTube oEmbed endpoint returned at time T.”**
  - Usually stored as `oembed.json`, but only if the endpoint returns HTTP 200.
- **“These are the exact bytes I received for the watch page / embed page at time T.”**
  - Often stored as `watch_headers_*.txt` / `watch_body_*.html`.
- **“This local MP4 was produced from these inputs, and here are the loudness / encode logs.”**
  - Often stored as `ffmpeg_i_stderr.txt`, loudnorm logs, and/or JSON.

Important: a bundle is evidence of **a specific observation**, not a promise that everyone will see the same result forever.

## Quick verify in ~60 seconds

1) **Download (or open) the bundle folder in this repo.**

2) **Verify checksums.**

On Linux:

```bash
cd /path/to/the/bundle
sha256sum -c SHA256SUMS.txt
```

On macOS:

```bash
cd /path/to/the/bundle
shasum -a 256 -c SHA256SUMS.txt
```

If every line says `OK`, the files match what I captured.

3) **(Optional) Re-run a request yourself.**

If the bundle includes a captured HTTP response, you can often reproduce a comparable fetch with `curl`. For byte-for-byte comparisons, I usually force **identity encoding**:

```bash
curl -i -H 'Accept-Encoding: identity' -L --max-time 30 \
  'https://www.youtube.com/watch?v=VIDEO_ID' \
  -o /tmp/watch_response.txt
```

Then you can hash your result:

```bash
sha256sum /tmp/watch_response.txt
# macOS: shasum -a 256 /tmp/watch_response.txt
```

Whether the bytes match depends on the site (see limitations below).

## Why I use `Accept-Encoding: identity`

Many servers will gzip/brotli responses by default. That’s good for bandwidth, but it complicates “exact bytes” proofs because:

- you might compare a compressed response to an uncompressed one
- range requests can behave differently on compressed payloads

So for proof captures I often send:

```http
Accept-Encoding: identity
```

That asks the server to return an uncompressed representation, making byte-for-byte comparisons much less ambiguous.

## Limitations (read this before over-trusting a bundle)

- **CDNs vary:** YouTube and other sites can serve different bytes by region, time, A/B test, logged-in state, etc.
- **oEmbed can lag:** Sometimes a video is watchable while oEmbed still returns 404 for a while.
- **Evidence, not a guarantee:** A bundle supports “I saw X at time T”, not “X is always true everywhere”.

## Where to read more in this repo

- Publish proof format: [`docs/publish_proof_bundle.md`](./publish_proof_bundle.md)
- YouTube oEmbed delays: [`docs/youtube_oembed_delay_notes.md`](./youtube_oembed_delay_notes.md)
