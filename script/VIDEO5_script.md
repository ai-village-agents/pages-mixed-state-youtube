# Video 5 — Cache-Control in the Wild: Browser vs CDN (max-age, s-maxage, no-cache, must-revalidate, stale-while-revalidate)

**Target length:** ~5–7 minutes. Tone: direct, practical, slightly investigative.

## Hook (first 10 seconds)
You push a fix. Your coworker on fast Wi‑Fi reloads and still sees the bug. You force-refresh and it’s gone—for you. The headers say `Cache-Control: max-age=300, s-maxage=30, stale-while-revalidate=120`.

## Core mental model: two caches
- There are **two independent caches** you care about: the **browser cache** on the viewer’s device and a **shared cache** at the edge (CDN/reverse proxy).
- `Cache-Control` directives tell caches **whether they can reuse a response without revalidation** and **for how long**. They don’t push new content; they govern reuse.
- **max-age** applies to any cache unless overridden. **s-maxage** overrides for shared caches (e.g., CDN). Browsers ignore `s-maxage`.
- **must-revalidate** means: after the freshness window, you must revalidate before reuse. If origin is down, you should not serve stale.
- **stale-while-revalidate** means a cache may serve a stale response **while** it fetches a fresh one in the background, within the given seconds.

## Mini-demo plan (curl -I)
Use a single URL with a predictable Cache-Control (or your staging page).

1) Inspect baseline headers (shows Age/freshness):
```bash
curl -I https://example.com/page.html
```

2) Confirm shared cache behavior vs browser cache:
```bash
# Force revalidation (good for probing a CDN edge)
curl -I -H 'Cache-Control: no-cache' https://example.com/page.html
```

3) Simulate “too old” (Age already high) and expect revalidation:
```bash
# After waiting > max-age, this should trigger revalidation
curl -I https://example.com/page.html
```

4) Show stale-while-revalidate in action (typical, not guaranteed):
```bash
# First request populates cache. Immediately hit again during background refresh.
curl -I https://example.com/page.html
sleep 1
curl -I https://example.com/page.html
```
- Watch `Age` and `Via`/`CF-Cache-Status` (or similar) to see if a shared cache served a stale response while refreshing.

## Scripted flow (spoken)
### 1) Why this matters (0:30)
- Mixed state isn’t just versions on disk; it’s also caches disagreeing about freshness.
- If you don’t know **which cache** is answering, you’ll overclaim.

### 2) The two-cache model (1:00)
- The browser cache is per-user, per-device. It follows `max-age`, `no-cache`, `must-revalidate`, `stale-while-revalidate` where supported.
- The CDN/shared cache is for everyone. It follows `max-age` unless `s-maxage` overrides.
- `Age` is a hint about the **shared cache** entry—your browser cache age is invisible from headers.

### 3) Reading Cache-Control in plain language (1:40)
- “You may reuse this for **max-age=N** seconds without checking.”
- “If you’re a **shared cache**, use **s-maxage=M** instead.”
- “After that window, **must-revalidate**: don’t serve stale unless you’ve confirmed freshness.”
- “If you support it, you may serve stale for **stale-while-revalidate=K** seconds while you fetch fresh.”
- `no-cache` = “you may store it, but you must revalidate before reuse.”

### 4) CDN vs browser interplay (3:00)
- With `Cache-Control: max-age=300, s-maxage=30`, a CDN might keep an object fresh for 30s, while browsers keep it fresh for 300s.
- If the CDN revalidates at 31s and gets new content, browsers that cached the old response can still reuse it for up to 300s unless told otherwise.
- `stale-while-revalidate` makes user experience smoother but can mask a brief deploy: users may see stale content while the CDN refreshes.
- `must-revalidate` reduces that risk by forcing caches to check before serving expired entries.

### 5) Walk through the curl mini-demo (3:50)
- First `curl -I` shows **Cache-Control**, **Age**, and any CDN hint headers.
- `-H 'Cache-Control: no-cache'` forces a revalidation path (still via cache).
- After waiting past `max-age`/`s-maxage`, `curl -I` should show `Age` reset or `CF-Cache-Status: REVALIDATED` (or similar).
- Two rapid hits with `stale-while-revalidate` often show one stale serve followed by fresh; call out that this is typical, not guaranteed.

### 6) Common traps (5:00)
- `no-cache` does **not** mean “no storage”; it means “revalidate before reuse.”
- `Age` reflects the shared cache entry, not your browser cache lifetime.
- `s-maxage` overrides `max-age` for shared caches; browsers ignore it.
- `stale-while-revalidate` can show old content while fetching new.
- `must-revalidate` is honored inconsistently across intermediaries—don’t assume it prevents all stale serves.
- Private content: `Cache-Control: private` stops shared caches, but browsers still cache unless `no-store` or short `max-age`.

### 7) Recap checklist (6:20)
- Identify which cache answered: look at `Age`, `Via`/`CF-Cache-Status`, and whether a CDN is in play.
- Read `Cache-Control` in full: `max-age`, `s-maxage`, `no-cache`, `must-revalidate`, `stale-while-revalidate`.
- Probe with `curl -I` plus optional `Cache-Control: no-cache` to force revalidation.
- When debugging deploys, log URL, time, status, Cache-Control, Age, validators (ETag/Last-Modified), and any CDN hints.
- Keep claims modest: behavior is **typical**, not guaranteed across CDNs and browsers.
