# Video 7 — YouTube metadata draft

Working title (internal): **Service worker: the cache you forgot**

## Title (draft)
**Service Worker: The Cache You Forgot (Debug “Old Version” Bugs)**

<details>
<summary>Other title options (kept for later)</summary>

- Service Workers Explained: Why Your Deploy Didn’t Update
- “I Deployed the Fix” — But My Browser Still Shows the Old Page (Service Workers)
- Service Worker Cache Debugging: Prove What You’re Actually Seeing
</details>

## Description (draft)
Ever deployed a fix… and *still* see the old page?

Sometimes it’s not your CDN cache. Sometimes it’s not your browser HTTP cache.

It’s a **service worker**.

A service worker can intercept requests inside its scope and respond from a cache it controls — which means:
- Two devices can hit the *same URL* and see different content
- A CLI check (`curl`) can disagree with what the browser renders (because `curl` doesn’t go through your browser’s service worker)

In this video we use a proof-first workflow:
- Prove whether a service worker is in the path
- Isolate the variable (private window / unregister / bypass)
- Compare variants (with SW vs without)
- Apply safer fix patterns

Tip: if your service-worker script is cached too aggressively, updates can get ‘stuck’. Serving `sw.js` with `Cache-Control: no-cache` (or versioning its URL) often helps.

## Chapters (draft)

Draft chapter timestamps based on the current slide timing (will change if timings change):

- 0:00 Service worker: the cache you forgot
- 0:13 Why this matters
- 0:26 What a service worker can do
- 0:40 How “two versions” happen
- 0:52 First proof: is SW in the path?
- 1:23 CLI vs browser (important)
- 1:36 Isolate the variable
- 1:54 Compare variants
- 2:07 Fix patterns (safer defaults)
- 2:30 Recap checklist
## Tags (draft)
service worker, service workers, pwa, cache debugging, stale content, old version, deploy not updating, web debugging, devtools, unregister service worker, cache storage

## Thumbnail direction (draft)
Goal: communicate **“old version”** + **service worker** as a distinct cache layer.

Option A:
- Big title: **SW** or **Service Worker**
- Subtext: **old version?**
- Small: **not CDN • not browser cache**

## Pinned comment (optional)
If `curl` shows the fix but the browser doesn’t, check whether a service worker is controlling the page and serving cached responses.
