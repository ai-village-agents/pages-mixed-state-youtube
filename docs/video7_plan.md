# Video 7 — plan (draft)

## Working title (internal)
**Service Workers: the cache you forgot**

## Why this topic
A huge class of “I deployed the fix but I still see the old page” bugs are not CDN or browser-cache issues — they’re **service-worker** caching and routing. It’s a different debugging surface area than `Cache-Control` / `Vary`.

## Target audience
Web developers who deploy SPAs / docs sites / PWAs and need a proof-first workflow.

## Core promise (what the viewer can do after)
**Prove** whether a service worker is in the request path, and then isolate it from other cache layers.

## Key claims (keep tight)
- A service worker can **intercept** network requests for its scope and respond from a cache it controls.
- A service worker can make “two versions” happen across:
  - devices/browsers (one has SW installed, one doesn’t)
  - sessions (one has old SW cached)
  - navigation paths (SW scope differences)
- `curl` does **not** go through the browser’s service worker, so CLI checks can disagree with what the browser shows.

## Proof-first debugging workflow (slide-level)
1. Symptom: same URL, different content
2. Ask: is a service worker installed?
3. Confirm interception:
   - DevTools signal like “from ServiceWorker” (wording differs by browser)
   - `navigator.serviceWorker.controller` presence (site JS console)
4. Isolate:
   - open a private window (often no prior SW state)
   - unregister SW (DevTools/Application) and hard reload
   - bypass SW (DevTools setting) if available
5. Compare:
   - browser-with-SW vs browser-without-SW
   - CLI `curl` vs browser fetch
6. Fix patterns:
   - versioning + cache-busting SW script itself
   - `skipWaiting()` / `clientsClaim()` carefully
   - short TTL for HTML shell; long TTL for hashed assets
7. Recap checklist

## Visual approach
- Slides only (like Videos 1–6).
- Use a 3-layer diagram: **CDN cache** ↔ **browser HTTP cache** ↔ **service worker cache**.
- Include 1–2 short code snippets (JS console + SW install/fetch pseudocode).

## Risks / things to avoid
- Don’t overclaim exact DevTools labels across browsers (say “look for an indicator like…”).
- Don’t imply SW is “always the cause”; frame as “common third layer.”
- Avoid security guidance beyond basics.
