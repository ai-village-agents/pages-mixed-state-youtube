# Video 3 — Cache-Busting Isn’t Proof: Read the Headers (Age / ETag / Cache-Control)

**Target length:** ~4–6 minutes. Tone: practical, cautious about claims.

## Hook
- Split-screen: ?cb=123 shows "new" layout, bare URL shows "old" layout. Viewers assume the query fixed it.
- Voiceover: "Changing the query string doesn’t prove anything—it can just send you to a different cache. Let’s read the headers instead."

## Thesis
- Cache-busting queries are a clue, not proof. The reliable evidence is in response headers (Status, Age, Cache-Control, ETag, Last-Modified, Via/CF-Cache-Status). Use curl to check before declaring victory.

## Slide list (9–11)
1) Title/hook: Cache-busting isn’t proof
2) Why ?cb helps but can mislead (different caches, stale still possible, masks split versions)
3) Where caches sit (browser, CDN edge, origin) — keep claims general
4) Minimal header checklist + commands we’ll use
5) HEAD example: `curl -I https://example.com/page.html`
6) GET with headers dumped: `curl -D - https://example.com/page.html`
7) Compare with/without cache-bust: `curl -I` on both URLs
8) Read the headers: what Status, Age, Cache-Control, ETag/Last-Modified, Via/CF-Cache-Status suggest
9) Recap: 4-step procedure
10) Caution/uncertainty: CDNs vary; gzip/range is covered in Video 2

## Key commands to show
```bash
curl -I https://example.com/page.html
curl -D - https://example.com/page.html
curl -I https://example.com/page.html
curl -I https://example.com/page.html?cb=now
```
(mention `-H 'Cache-Control: no-cache'` as optional probe, but note it can bypass caches.)

## What the viewer learns
- Why `?cb=` alone doesn’t prove freshness and can mask split states.
- A quick header-reading checklist to tell cached vs fresh responses.
- How to run curl probes (HEAD vs GET dumping headers) and compare two URLs.
- To keep claims modest about CDNs/GitHub Pages internals; focus on observable headers.

## Caveats to state on-camera
- Different CDNs expose different `Via`/`CF-Cache-Status`-style headers; absence doesn’t prove anything.
- `Cache-Control: no-cache` forces revalidation but may still serve cached content; it’s a probe, not a guarantee.
- gzip/range sampling pitfalls are covered in Video 2 (link back, don’t rehash).
