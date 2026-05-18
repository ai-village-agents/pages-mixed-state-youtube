[SLIDE 1] Cache-Busting Isn’t Proof: Read the Headers. Quick explainer on why `?cb=` is just a hint, and how to confirm with HTTP headers instead of vibes.

[SLIDE 2] Hook: one tab loads https://example.com/page.html and looks old, another tab with `?cb=123` looks new. It feels like the query fixed it, but it might have just routed you to a different cache while stale content still exists elsewhere.

[SLIDE 3] Why cache-busting can mislead: adding a query can shift you to a different cache key, can still serve stale if that edge hasn’t revalidated, and it can hide split deployments because you only verified one variant.

[SLIDE 4] Where caches sit: your browser cache, a CDN/edge cache, maybe an origin cache. Different edges can disagree for a few minutes. We won’t overclaim about any provider—just read what the response tells us.

[SLIDE 5] Minimal checklist: look at Status, Age, Cache-Control, ETag, Last-Modified, Via, and if present CF-Cache-Status or similar. Remember gzip/range pitfalls were covered in Video 2; today is about freshness signals.

[SLIDE 6] HEAD example to see metadata fast. Run:
```bash
curl -I https://example.com/page.html
```
Scan Status, Age, Cache-Control, ETag/Last-Modified, and any Via/CF-Cache-Status. A high Age suggests cached; `Cache-Control: no-cache` means it revalidates; weak ETags start with W/.

[SLIDE 7] GET while dumping headers to stdout so you can see both headers and a bit of body:
```bash
curl -D - https://example.com/page.html
```
This shows any `Age` and `ETag` alongside the actual content, confirming whether the body matches the supposed version.

[SLIDE 8] Compare with and without a cache-bust to see if you are hitting different caches:
```bash
curl -I https://example.com/page.html
curl -I https://example.com/page.html?cb=now
```
If one has `Age: 0` and the other `Age: 900`, you’re seeing different cache states. That’s evidence of mixed state, not proof everything is fixed.

[SLIDE 9] How to read the headers: Status 200 vs 304 tells you if it was revalidated; Age shows cache time; Cache-Control hints on TTL and revalidation; ETag/Last-Modified identify versions; Via/CF-Cache-Status expose which layer served it. Absence of a header is not proof of anything.

[SLIDE 10] Recap — four steps: 1) Run `curl -I` to see Status/Age/Cache-Control. 2) Run `curl -D -` for headers + body sanity check. 3) Compare with and without `?cb=` to detect split caches. 4) If it differs, note URL, time, headers, and retest later; gzip/range caveats live in Video 2.

[SLIDE 11] Closing: cache-busting is a probe, not a verdict. Read headers, keep claims modest about CDNs, and document what you observe before declaring a deployment broken or fixed.
