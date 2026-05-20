# Video 6 — YouTube metadata draft

Working title (internal): **Vary: the cache key you forgot**

## Title (selected)
**Vary: The Cache Key You Forgot (Debug “Two Versions” Bugs)**

<details>
<summary>Other title options (kept for later)</summary>

- Vary Header Explained: Why You See a Different Page
- Stop Guessing “Stale”: Check Vary (Cache Debugging)
</details>

## Description (draft)
Ever had a “stale page” bug where you and your coworker load the *same URL*… but see *different content*?

Often it’s not randomness—it’s **variants**.

When a response includes a `Vary` header, caches treat the object as:

> **cache key = URL + the request headers listed in `Vary`**

Change those headers (language, encoding, cookies, user agent…), and you can land in a different cached bucket.

In this video, we focus on a proof-first debugging workflow:
- Read `Vary` and validators (`ETag`, `Last-Modified`)
- Probe with `curl` using alternate request headers
- Save **two header dumps** and `diff` them
- Treat “cache-busting” query params as hints, not proof

### Commands shown
```bash
curl -I https://example.com/page
curl -I -H 'Accept-Language: en-US' https://example.com/page
curl -I -H 'Accept-Language: fr-FR' https://example.com/page
curl -I -H 'Accept-Encoding: identity' https://example.com/page
curl -I -H 'Accept-Encoding: gzip' https://example.com/page

curl -sD en.headers -o /dev/null -H 'Accept-Language: en-US' -H 'Accept-Encoding: identity' https://example.com/page
curl -sD fr.headers -o /dev/null -H 'Accept-Language: fr-FR' -H 'Accept-Encoding: identity' https://example.com/page

diff -u en.headers fr.headers
```

(Examples use `example.com`—apply the same steps to your real URL.)

## Chapters (draft)
From the final concat durations (recommended):
- 0:00 Vary: the cache key you forgot
- 0:15 Why this matters
- 0:33 What Vary does
- 0:49 Common splitters
- 1:05 How two versions appear
- 1:30 Query params ≠ proof
- 1:46 Proof mindset
- 2:05 Command: probe variants
- 2:28 Command: save & diff headers
- 2:46 Read what changes
- 3:05 Reduce surprises
- 3:22 Recap checklist

## Tags (draft)
vary header, http caching, cache key, cdn cache, browser cache, cache-control, etag, last-modified, curl, web debugging, stale content, content negotiation, accept-language, accept-encoding, gzip, brotli, cloudflare cache, fastly, github pages

## Thumbnail direction
Goal: instantly communicate “same URL, different results” + the word **Vary**.

Option A (minimal, based on Slide 1):
- Big title: **Vary**
- Subtext: **same URL • different page?**
- Visual: darkened bottom bar behind the headline; top-left bullets kept small.

Option B (more technical):
- Big title: **Vary**
- Subtext: **cache key ≠ just URL**
- Visual: URL + “+ Accept-Language + Accept-Encoding” as a key/fingerprint.

## Pinned comment (optional)
If you’re debugging “stale” content, start by saving two header dumps and diffing them. HTML can mislead; headers usually won’t.
