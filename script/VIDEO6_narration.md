## Slide 1 — Vary: the cache key you forgot
Your coworker sees Spanish text. You see English. Same URL, same deploy, no feature flags. Before you assume “stale cache,” check one header: Vary. Vary is how one URL legitimately becomes multiple cached objects.

## Slide 2 — Why this matters
This isn’t rare. One person can be routed to a different language, a different compression variant, a different AB test cohort, or even a different device experience. And in real systems, both the CDN and the browser can each store more than one version at the same time.

## Slide 3 — What Vary does
Vary expands the cache key. The cache key isn’t just the URL. It’s the URL plus the request headers listed in Vary. If the response says `Vary: Accept-Language`, then the cache is supposed to keep separate buckets per language header, so it stays correct.

## Slide 4 — Common splitters
The usual splitters are Accept-Language, Accept-Encoding, User-Agent, and Cookie. Sometimes you’ll also see custom headers like X-Region or X-Device. Each one is a potential “two versions of the same page” generator.

## Slide 5 — How two versions appear
Here’s the pattern. If `Vary: Cookie` is present, an AB-test cookie can fork responses. If `Vary: Accept-Encoding` is present, you can end up with separate gzip, brotli, and identity copies. And if Accept-Language varies, you can have parallel localized pages. That’s not a bug — it’s the cache doing what it was told.

## Slide 6 — Query params ≠ proof
When you see `?cachebust=123`, treat it as a clue someone suspected caching. It does not prove which cache answered, or which variant you’re currently hitting. Query params can change the URL, but they don’t explain header-based variants.

## Slide 7 — Proof mindset
So switch to proof mode. Capture headers and compare them side by side: ETag, Age, Cache-Control, Vary, and Content-Encoding. CDN hints like CF-Cache-Status or X-Cache are supportive evidence, but they’re not always consistent across providers.

## Slide 8 — Command: probe variants
Start with a baseline HEAD request to see what the server claims it varies on. Then probe one header at a time.

If you change Accept-Language and the ETag changes, that’s a strong sign you’re seeing different cached variants. For compression, I prefer an explicit baseline like `Accept-Encoding: identity`, and then compare it to `Accept-Encoding: gzip`.

## Slide 9 — Command: save & diff headers
And here’s the repeatable part: save your response headers to files, then diff them. This is why I like `curl -sD file -o /dev/null` — it’s a GET, but you discard the body.

If a server behaves differently on HEAD versus GET, this avoids that pitfall while still keeping your proof lightweight.

## Slide 10 — Read what changes
What should you look for? If ETag differs between probes, you probably hit distinct variants. If Age behaves differently per probe, you’re likely hitting separate cache buckets. And if Content-Encoding swaps when you change Accept-Encoding, that’s a very direct signal of variant splitting.

## Slide 11 — Reduce surprises
If you own the system, the fix is often reducing unnecessary variation. Minimize Vary to the fields you truly need. Normalize noisy headers at the edge when possible. And if you know you have critical variants, warm them intentionally after deploys.

## Slide 12 — Recap checklist
Recap: check Vary before assuming “stale.” Probe variants with curl using alternate headers. Save and diff headers so you’re not arguing from vibes. And remember: cache-busting parameters are hints, not proof.
