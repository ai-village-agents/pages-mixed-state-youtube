# Video 5 — YouTube metadata (draft)

## Title (option A)
Cache-Control in the Wild: Browser Cache vs CDN Cache (Debug the “why do I still see it?” problem)

## Title (option B)
Cache-Control: Why Your Coworker Still Sees the Bug (Browser cache vs CDN cache)

## Description (draft)
You ship a fix, refresh, and it’s gone… but your coworker still sees the bug.

This is usually a **two-caches** problem:
- a **browser cache** (per user)
- a **shared cache/CDN** (for everyone)

In this video, we’ll translate Cache-Control into plain language so you can answer:
- **which cache answered** (browser vs CDN)
- **why it answered** (reuse window, revalidation, or stale-while-revalidate)

Practical checklist:
- log URL + time + status
- read `Cache-Control` (and `Age` if present)
- check validators (`ETag` / `Last-Modified`)
- watch for CDN hints

(If you’ve ever relied on “hard refresh” as a debugging step, this is the mental model that makes it make sense.)

## Chapters (based on slide timings)
00:00 Hook + promise
00:22 Two caches (browser vs CDN)
01:13 Plain-language Cache-Control directives
02:12 How CDN vs browser can diverge
02:54 Demo commands (curl: Cache-Control / Age / ETag)
03:07 Common traps (no-store, shared caches, background fetch)
03:58 Practical checklist

## Tags (draft)
cache-control, http caching, cdn, browser cache, etag, last-modified, age header, stale-while-revalidate, must-revalidate, max-age, s-maxage, debugging
