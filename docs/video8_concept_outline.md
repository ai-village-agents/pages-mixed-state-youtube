# Hard Reload Isn’t Proof: A Browser Cache Checklist (With curl Controls)

Audience: web devs who are stuck seeing an old version after deploy and need a proof-first way to show which cache is lying.

## Why “I hit hard reload” isn’t evidence
Hard reload only bypasses parts of the browser HTTP cache for the active tab. It does not evict CDN objects, server caches, or service worker responses. To prove where the stale bytes come from, you need a layered plan with captured evidence.

## The 3-layer model and how to isolate each
Layer 1: **Server/CDN** (origin, reverse proxy, CDN edge)
- What it does: content negotiation, compression, cache keys, TTLs, revalidation, sometimes HTML rewriting.
- How to isolate: fetch without a browser to avoid tab state; force no conditional headers from you; check response headers and entity digests.
- Minimal test: `curl -I` (or `-i` when you need body) to each public URL you suspect is stale. Capture `Cache-Control`, `ETag`, `Last-Modified`, `Vary`, and any CDN-specific headers (e.g., `CF-Cache-Status`, `Age`). Repeat with and without `--compressed` to see what encoding is negotiated; compression can change the cache key and content hash.

Layer 2: **Browser HTTP cache** (per-profile, per-origin, respects Vary)
- What it does: stores decoded resources keyed by URL + Vary dimensions. Hard reload bypasses it for the tab but doesn’t delete entries or affect other tabs.
- How to isolate: open a **new private window** so there’s no prior cache; fetch once to prime, then fetch again to see if you get a 200 vs 304 and whether content changes. Avoid devtools “disable cache” while testing because it forces different headers than real users send.
- Minimal test: in the private window, load URL A twice and watch status codes and `ETag` behavior. Separately, fetch the same URL via curl (outside the browser) to compare headers and body digests.

Layer 3: **Service worker cache** (Cache Storage + fetch event logic)
- What it does: can intercept any request and return cached responses regardless of HTTP headers; its own cache key rules may differ from the network URL.
- How to isolate: disable/skip the service worker or test in a profile with service workers disabled. In Chrome: Application panel → Service Workers → “Bypass for network.” Alternatively, fetch the same URL from curl and from a private window with service workers unregistered; compare bodies and digests.
- Minimal test: with “Bypass for network” enabled, reload and note if the body/hash now matches origin. If yes, stale content was from the service worker path.

## A short command set for capture
Use a stable shell block and copy results into your proof bundle:

```bash
# 1) Headers only (identity encoding)
curl -I --header 'Accept-Encoding: identity' https://example.com/path

# 2) Headers + body with compression negotiation
curl -i --compressed https://example.com/path -o /tmp/path.compressed

# 3) Compare identity vs compressed hashes (after decompression)
curl --header 'Accept-Encoding: identity' https://example.com/path -o /tmp/path.identity
sha256sum /tmp/path.identity /tmp/path.compressed

# 4) Alternate URL (e.g., CSS/JS asset) to see if cache keys differ
curl -I --compressed https://example.com/app.css
```

Caveat: `--compressed` asks for gzip/br. Some CDNs cache per encoding; if you skip `Accept-Encoding: identity`, you might hit a different object than the one the browser cached. Always record which encoding you negotiated.

Vary note: If `Vary: Accept-Encoding, Cookie` appears, two users may see different cache objects. If you test with cookies present, record that.

Private window control: open a new private window, load the same URL twice, and record the first/second status codes and final body hash; that gives you the browser-cache view without extensions or old entries.

## Proof bundle (what to capture and how to name)
Goal: produce a small, verifiable package another engineer can replay without your browser.

- **Headers**: save raw headers for two URLs (typically HTML entry + one critical asset). Use `curl -I --header 'Accept-Encoding: identity'` and `curl -I --compressed`. Name files `headers.identity.<slug>.txt` and `headers.compressed.<slug>.txt` where `<slug>` is `html` or `app-css`.
- **Bodies**: save full bodies for the same URLs, one identity and one compressed negotiation. Name `body.identity.<slug>.bin` and `body.compressed.<slug>.bin`.
- **Hashes**: run `sha256sum` on every saved body. Put results in `sha256.<slug>.txt`. Include the command you ran at the top of the file. Hashes allow diffing even when bodies are large or binary.
- **Context note**: inside each text artifact, prepend a short note: timestamp, URL, and whether the request came from private window, normal tab, or curl. This removes ambiguity when someone else reads it.
- **Optional SW check**: if you toggled “Bypass for network,” note that in a one-line file `sw-mode.txt` so reviewers know whether service worker interception was in play.

Packaging suggestion: place everything under `proof-bundle/<date>-<env>/` (e.g., `proof-bundle/2024-05-20-prod/`). That directory should stand alone as evidence: headers, bodies, hashes, and a README with the exact curl commands and browser mode.

## How to walk the sequence (minimal steps)
1) Run the curl set twice: once with `Accept-Encoding: identity` and once with `--compressed`. Save headers and bodies; hash both.
2) In a new private window, load the same URLs twice. Note status codes and final rendered version (e.g., app version string, build id).
3) Toggle “Bypass for network” (service worker off) and repeat the private-window load. If the version changes only now, the service worker cache was stale.
4) Compare hashes: if curl identity vs browser differ, the stale layer is likely server/CDN or SW. If browser repeat fetch returns 304 but hash changes, the browser cache obeyed headers but content changed—flag server inconsistency.
5) Summarize in the proof bundle README which layer changed when you flipped each control (encoding, private window, SW bypass).

## 20-second checklist CTA
- New private window: load twice; record status codes and version string.
- Service worker bypass on: reload; did the version change? Note it.
- curl `-I` with `Accept-Encoding: identity` and `--compressed`: save headers.
- curl bodies for HTML + one asset; hash them (`sha256sum`); save.
- Store everything under `proof-bundle/<date>-<env>/` with notes on browser mode and encoding.
- If a toggle flips the version, you found the guilty layer—attach that bundle to your deploy ticket.
