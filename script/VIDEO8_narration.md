# Video 8 — narration (draft)

## Slide 1 — Hard reload isn’t proof
If you’re debugging a deploy and someone says, “I hard reloaded and it’s still old,” that’s not proof on its own.

Three layers can show the same URL differently: the network (server or CDN), the browser HTTP cache, and a service worker.

The fix depends on which one you’re fighting, so we need evidence, not vibes.

## Slide 2 — What a hard reload really does
A hard reload skips most browser HTTP cache for that tab — that’s it.

It still lets a CDN, reverse proxy, or service worker answer.

So “I hard reloaded” can still deliver cached HTML, cached JS, or a service worker-controlled response.

## Slide 3 — Minimal reproducible check
Pick a known string or version, like `version=2024.06.15-build42`, and have everyone read the exact same URL.

Log which layer served it: note headers like `Age`, `Via`, or service worker indicators.

Agreeing on a single artifact keeps the investigation reproducible.

## Slide 4 — "First proof: raw fetch"
Start with curl as your control. Request identity encoding so you see true lengths and headers:

`curl -i https://example.com/ --header 'Accept-Encoding: identity'`

Save the response and headers — they tell you whether origin, CDN, or something else answered.

## Slide 5 — Compare encodings
Run two hashes to detect variants or caching differences:

`curl --compressed -s https://example.com/ | sha256sum`
`curl -s --header 'Accept-Encoding: identity' https://example.com/ | sha256sum`

If the hashes differ, you’re seeing different content or encodings; if they match, the bytes align.

## Slide 6 — Check the HTML entry point
HTML decides which JS bundle the app loads.

If HTML is stale, you may never request the new bundle.

Always verify the HTML response carries the expected version string before chasing asset caches.

## Slide 7 — Service worker vs CDN vs browser
Identify who answered:

- Service worker: `navigator.serviceWorker.controller` is non-null, or DevTools shows “from ServiceWorker.”
- CDN: headers like `Via`, `Age`, or `X-Cache` hint at the edge node.
- Browser: DevTools “from disk cache” or “memory cache” tells you local cache was used.

That split prevents blaming the wrong layer.

## Slide 8 — Isolate state
Change state on purpose to isolate the culprit.

Private window to drop stored service worker control and cache; different network (cell vs office VPN) to hit another CDN edge.

If DevTools allows, bypass the service worker; otherwise unregister, then reload to confirm the controller is gone.

## Slide 9 — Experiment matrix
Lay out a small matrix: Browser A with a service worker vs Browser B without; Edge location X vs Y; hard reload vs cache cleared vs curl identity.

Record the responses and headers in a tiny table so you can compare like-with-like.

That table is your audit trail and makes fixes testable.

## Slide 10 — Fix and verify
Fix the source: bust HTML aggressively with short TTL or `Cache-Control: no-cache` so new shells ship quickly.

Version service workers and assets; update scopes intentionally so old controllers retire.

Re-run the curl comparisons and confirm the visible version string updates in the HTML and UI.

## Slide 11 — Decision tree (screenshot this)
Here’s the quick decision tree:

- Curl with identity shows old: server, CDN, or origin still serving old.
- Curl shows new but browser shows old: browser HTTP cache or headers keeping it.
- Curl shows new and browser shows new but app acts old: service worker path.

curl first, then browser cache, then service worker.
