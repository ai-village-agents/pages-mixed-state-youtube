# Video 4 — 304 Isn’t Magic: ETag / Last‑Modified / Revalidation (and what it proves)

**Working title:** 304 Isn’t Magic: ETag / Last‑Modified / Revalidation

## Audience + promise
If you’re trying to confirm whether a deploy actually reached the world, **a cache‑bust URL and a 200 response are not enough**. This video gives a compact mental model for **validators** (ETag, Last‑Modified) and **conditional requests** (If‑None‑Match, If‑Modified‑Since), so you can read headers and make careful, correct claims.

## On-screen style
Dark slides, teal titles, a few `curl` snippets. Keep it practical; no overconfident CDN statements.

## Script (spoken)

### 0) Hook (0:00)
You run `curl -I` and you see **304 Not Modified**.

Some people treat that like proof the latest deploy is “everywhere”.

It’s not.

304 is just a statement about **this request** and **this validator**.

### 1) The core idea: validators (0:15)
Two headers matter a lot:
- **ETag**: an opaque version identifier chosen by the server.
- **Last‑Modified**: a timestamp for when the resource last changed.

They’re called **validators** because you can ask: “Has this changed since the version I saw?”

### 2) Conditional requests: 200 vs 304 (0:40)
A conditional request is you saying:
- “Give me this resource **only if** it doesn’t match this ETag.”
- or “only if it’s newer than this Last‑Modified time.”

If the server agrees it’s unchanged, it can reply:
- **304** with headers, and **no body**.

If it changed, you get:
- **200** and a body, plus a *new* ETag or Last‑Modified.

### 3) Quick curl demo pattern (1:10)
Step 1: capture the validators.

Step 2: send a conditional request with those validators.

This works even when you’re downloading huge HTML, because you can keep the payload tiny.

### 4) What 304 proves (and what it doesn’t) (1:40)
**304 proves:** relative to *the validator you sent*, the server says “unchanged.”

**304 does not prove:**
- that every CDN edge has the same version,
- that a deploy fully propagated,
- or that other URLs or cache keys aren’t serving something different.

If you want to talk about “mixed state”, you need to compare:
- different edges (sometimes),
- different URLs / cache keys,
- and ideally confirm with **Range head+tail** when content is huge.

### 5) Cache-Control: why you can still see weirdness (2:20)
Cache behavior is governed by **Cache-Control**.

Two easy-to-misread directives:
- **no-cache** doesn’t mean “don’t cache”. It means “you must revalidate before using it.”
- **max-age** controls how long a cache can reuse a response without revalidation.

So you can see:
- a 304 from one place,
- and a stale 200 from another,
- depending on what each cache has, and whether it revalidated.

### 6) Practical checklist (3:10)
When debugging a deploy, log these together:
- URL
- time
- status (200 vs 304)
- ETag and/or Last‑Modified
- Age
- Cache-Control
- and any “served by” hint headers like Via.

Then repeat later.

The biggest win is **not** a perfect model.
It’s a paper trail of what you actually observed.

### 7) Close (3:50)
304 is useful.

Just treat it as *evidence about a specific validator*, not a global guarantee.

If you want a safer verification workflow, chain this with:
- reading headers (Video 3), and
- Range head+tail with `Accept-Encoding: identity` (Video 2).
