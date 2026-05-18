# Video 2 — "Range Requests Without Lying to Yourself" (GitHub Pages / huge HTML)

**Target length:** 4–6 minutes

## 00:00 Hook — "I only downloaded 4 KB… so why is it gibberish?"
- Quick demo: `curl -r 0-4095 https://…` and the output looks garbled / incomplete.
- Promise: a reliable pattern for sampling *huge* HTML without accidentally reading compressed bytes as text.

## 00:25 What HTTP Range actually means (the 10-second version)
- Range is **bytes**, not "characters".
- Servers may send either:
  - uncompressed bytes (identity), or
  - compressed bytes (gzip/br), depending on `Accept-Encoding`.

## 01:05 The common pitfall
- You request a byte range… but you’re ranging the **compressed stream**.
- Result: the slice doesn’t correspond to the top/bottom of the *decoded* HTML.

## 01:35 The reliable checklist (copy/paste)
1) First: check if the server honors ranges.
```bash
curl -sI https://user.github.io/site/ | egrep -i 'accept-ranges|content-encoding|content-length'
```

2) Force identity (no gzip) for sampling.
```bash
curl -sI -H 'Accept-Encoding: identity' https://user.github.io/site/ \
  | egrep -i 'accept-ranges|content-encoding|content-length'
```

3) Head sample:
```bash
curl -s -H 'Accept-Encoding: identity' -r 0-4095 https://user.github.io/site/
```

4) Tail sample:
```bash
curl -s -H 'Accept-Encoding: identity' -r -4096 https://user.github.io/site/
```

## 02:40 Optional: detect "two versions" quickly
- If you expect a version stamp, search both samples for it.
```bash
curl -s -H 'Accept-Encoding: identity' -r 0-8191  https://… | rg -n 'version|build|id:'
curl -s -H 'Accept-Encoding: identity' -r -8192 https://… | rg -n 'version|build|id:'
```

## 03:20 Safety notes (don’t overclaim)
- A single head/tail sample is evidence of *served bytes at that time*, not proof of the entire document.
- If content is inconsistent: record time + URL + headers.

## 04:10 Closing
- One-liner summary: **Range is bytes; disable gzip when you want readable samples.**
- Link to repo + Video 1.

## Links
- MDN: https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests
- curl: https://curl.se/docs/
