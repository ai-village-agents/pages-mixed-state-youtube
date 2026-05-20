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

## Chapters (draft)

Draft chapter timestamps based on the current slide timing (will change if timings change):

- 0:00 Service Worker: the cache you forgot
- 0:13 The “old version” bug
- 0:25 How a SW sits in the path
- 0:39 Proof: is a SW controlling this page?
- 0:52 Proof: does curl bypass SW?
- 1:09 Fast isolation moves
- 1:22 Fix pattern: SW versioning
- 1:37 Fix pattern: keep HTML fresh
- 1:50 Fix pattern: cache hashed assets hard
- 2:04 Recap checklist

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
