## Slide 1 — Cache-Control in the Wild
Ship a fix, your coworker reloads and still sees the bug. You hard refresh and it disappears. The response shows Cache-Control with max-age 300, s-maxage 30, stale-while-revalidate 120. In the next few minutes, we’ll figure out which cache lied to you.

## Slide 2 — Two caches
There are two independent caches you care about: the browser cache on the viewer’s device and a shared cache at the edge, like a CDN or reverse proxy. Cache-Control tells caches whether they can reuse a response without revalidation and for how long. It doesn’t push new content; it governs reuse. Think about two separate behaviors: the browser cache is per-user, per-device, and follows max-age, no-cache, must-revalidate, and stale-while-revalidate where supported. The CDN or shared cache is for everyone and follows max-age unless s-maxage overrides it. Age is added by caches and means “this response has been sitting here for N seconds since it was generated or last validated.” Browsers usually don’t expose their local cache age with an Age header; CDNs often do.

## Slide 3 — Plain-language directives
max-age applies to any cache unless something overrides it. s-maxage overrides for shared caches; browsers ignore it. must-revalidate means that after the freshness window you’re supposed to revalidate before reuse; it does not force checks during max-age, and real intermediaries vary. stale-while-revalidate means a cache may serve a stale response for the stated seconds after max-age while it fetches fresh in the background—if it implements that directive. Read Cache-Control in plain language. “You may reuse this for max-age equals N seconds without checking.” “If you’re a shared cache, use s-maxage equals M instead.” “After that window, must-revalidate: once freshness expires, revalidate before reuse, if the intermediary enforces it.” “If you support it, you may serve stale for stale-while-revalidate equals K seconds beyond max-age while you fetch fresh in the background.” And no-cache means you may store it, but you must revalidate before reuse.

## Slide 4 — How CDN vs browser diverge
Here’s how the browser and CDN interplay with Cache-Control: with max-age 300 and s-maxage 30, a CDN might keep an object fresh for 30 seconds, while browsers keep it fresh for 300. If the CDN revalidates at 31 seconds and gets new content, browsers that cached the old response can still reuse it for up to 300 seconds unless told otherwise. stale-while-revalidate makes user experience smoother but can mask a brief deploy because a cache may serve stale during the background refresh if it implements SWR. must-revalidate kicks in only after freshness ends; it’s the intent, but not all intermediaries honor it.

## Slide 5 — Diagram
Picture the flow: browser cache to CDN or edge to origin, with Cache-Control, Age, and validators flowing back down.

## Slide 6 — Demo commands
Let’s walk through a quick curl probe. First, run curl dash I on the URL to see Cache-Control, Age, and any CDN hints; curl bypasses your browser cache entirely, so you’re inspecting the network. Then send curl dash I with an added header, Cache-Control: no-cache, to ask caches to revalidate before reuse; some may still behave differently, so you’re probing real behavior. After waiting past max-age or s-maxage, run curl dash I again and watch whether Age resets or a header like CF-Cache-Status shows a revalidation. To spot stale-while-revalidate in action, prime the cache with curl dash I, then hit it again immediately; if the cache supports SWR, you might see one stale serve while it refreshes in the background, then a fresh one.

## Slide 7 — Common traps
Common traps: no-cache does not mean no storage; it means revalidate before reuse. Age reflects how long the cached response has lived; browsers usually don’t emit it, CDNs often do. s-maxage overrides max-age for shared caches; browsers ignore it. stale-while-revalidate may show old content while fetching new, if the cache implements it. must-revalidate applies after expiry; honoring it varies—don’t assume it prevents all stale serves. For private content, Cache-Control: private stops shared caches, but browsers still cache unless you say no-store or use a short max-age.

## Slide 8 — Practical patterns
Practical patterns I ship: HTML or doc pages often get a short max-age or no-cache plus validators like ETag or Last-Modified so revalidation is quick. Fingerprinted static assets like app dot abc123 dot js get very long max-age equals 31536000 with immutable where supported, relying on the filename change to update. Sensitive responses often use no-store and sometimes private to avoid unintended caching.

## Slide 9 — When this model breaks
Where this model breaks: service workers, app caches, or heavy SPA bundling can short-circuit normal HTTP cache semantics. Multiple CDNs or layered proxies can add hops where directives or enforcement differ.

## Slide 10 — Recap checklist
Quick recap. Identify which cache answered: look at Age, Via or CF-Cache-Status, and whether a CDN sits in front. Read Cache-Control fully: max-age, s-maxage, no-cache, must-revalidate, stale-while-revalidate. Probe with curl dash I plus an optional Cache-Control: no-cache to force revalidation. When debugging deploys, log the URL, time, status, Cache-Control, Age, validators like ETag or Last-Modified, and any CDN hints. Keep claims modest: this behavior is typical, not guaranteed across CDNs and browsers.
