# Video 6 — Vary: the cache key you forgot (and how it creates “two versions” in the real world)

**Target length:** ~4–6 minutes. Tone: practical, skeptical, friendly.

## Cold open (15–25s)
Your coworker sees Spanish text; you keep seeing English. Same URL, no feature flags. You both hard refresh; nothing changes. The headers show `Vary`, and now you're wondering if the cache built two different versions of the page.

## Section 1: What Vary really does
- Caches key on **URL + request headers named in Vary**. Change the headers, you can hit a different bucket even on the same URL.
- Common culprits: `Accept-Language`, `Accept-Encoding`, `User-Agent`, `Cookie`, sometimes custom `X-Region`.
- If the origin sets `Vary: Accept-Language, Cookie`, a CDN could hold multiple variants at once; browsers can also store variants.
- Cache-busting query params (`?v=123`) are a clue that someone hit caching trouble, **not proof** of what's happening right now.

## Section 2: How two versions show up in real life
- Person A has `Accept-Language: en-US`, Person B has `fr-FR`; the CDN serves two language variants because `Vary: Accept-Language` is present.
- Mobile User-Agent vs desktop User-Agent when `Vary: User-Agent` exists can split caches.
- Cookies are brutal: a stray AB-test cookie on one user but not the other will fork the cache when `Vary: Cookie` is set.
- Mixed compression: if `Vary: Accept-Encoding` is set, a cache can have gzip, brotli, and identity copies. For controlled comparisons, explicitly set `Accept-Encoding: identity` as a baseline. (`curl --compressed` is convenient for “browser-like” behavior, but it auto-adds encodings and may hide details by decompressing.)
- The result: coworker hits one variant, you hit another; deploys can warm some variants but not others.

## Section 3: How to prove it (not just guess)
- Compare **headers**, not HTML eyeballing: capture `ETag`, `Age`, `Cache-Control`, `Vary`, `Content-Encoding` for each request.
- Baseline and variant curls (swap headers, same URL):
```bash
# Baseline: see what Vary lists
curl -I https://example.com/page

# Language variant probe (forces CDN to consider a different bucket)
curl -I -H 'Accept-Language: en-US' https://example.com/page
curl -I -H 'Accept-Language: fr-FR' https://example.com/page

# Compression variant probe (explicit is easier to reason about)
curl -I -H 'Accept-Encoding: identity' https://example.com/page
curl -I -H 'Accept-Encoding: gzip' https://example.com/page
```
- If the ETag or Age differs between these requests, you're likely hitting different cached variants. If ETag is same but Age differs wildly, you might be hitting different cache nodes or buckets.
- Watch for CDN hints (`CF-Cache-Status`, `X-Cache`) changing between header sets. A miss followed by a hit on the second command suggests a separate variant was filled.
- Proof mindset: save both header dumps and compare; don't rely on "the HTML looks different."
- If someone added `?cachebust=1`, treat it as a signal to inspect Vary and headers; it's a clue, not proof, that caching is involved.

## Recap + actionable checklist
- **Vary expands the cache key** beyond the URL; differing request headers can create parallel versions.
- **Common splitters**: Accept-Language, Accept-Encoding, User-Agent, Cookie, custom region headers.
- **Check headers, not vibes**: compare ETag, Age, Cache-Control, Vary, Content-Encoding between requests.
- **Use curl with alternate headers** to probe variants: language, compression, User-Agent, cookies.
- **Query params help but don't prove** caching issues; verify with header comparisons.
- **When debugging**, log URL, time, request headers you sent, plus the full response headers; keep both variants side-by-side to avoid chasing ghosts.
