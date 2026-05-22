# Video 8 — Beat sheet (draft): “Hard Reload Isn’t Proof”

**One-sentence promise:** In ~3–6 minutes, learn a *decision-flow* to tell whether “old version” is coming from (1) server/CDN, (2) browser HTTP cache, or (3) a service worker—using curl as a control.

## 0) Hook (0:00–0:20)
- “If you’re debugging a deploy and someone says ‘I hard reloaded and it’s still old’—that’s not proof.”
- Ever deployed a fix, hard reloaded, and still saw the old version? Same symptom, different causes.

## 1) The 3-layer model (0:20–0:45)
- Layer A: **Server/CDN** (what the network returns)
- Layer B: **Browser HTTP cache** (ETag/304, Cache-Control)
- Layer C: **Service worker** (can serve responses *without hitting the network*)

## 2) Step 1 — Establish a network control with curl (0:45–1:30)
- Fetch the URL with **identity encoding** and save bytes.
- Hash the body (sha256) so we’re comparing reality, not vibes.
- Key line: “Before we touch the browser, prove what the origin/CDN is serving.”

## 3) Step 2 — Sanity-check: is the *network* inconsistent? (1:30–2:10)
- Repeat curl.
- If hashes differ: it’s likely server/CDN propagation, geo variance, or dynamic responses.
- If hashes match: the network is stable; now we can blame the browser stack.

## 4) Step 3 — Browser HTTP cache checks (2:10–3:00)
- DevTools → Network: enable “Disable cache” (while DevTools is open) and reload.
- Look at response headers (examples vary): Cache-Control, ETag, Age, Via, CF-Cache-Status.
- Emphasize: hard reload is a *behavior*, not a guarantee; caches can still win.

## 5) Step 4 — Service worker checks (3:00–4:10)
- DevTools → Application → Service Workers:
  - Is there a controller?
  - Try “Update”, “Skip waiting”, or unregister.
  - Reload and confirm whether the controller is gone.
- Key line: “If a service worker is controlling the page, it can serve old bytes even when the network is new.”

## 6) Teaser + prevention payoff: visible version strings (4:10–4:50)
- Add a visible version marker (footer/build id) so humans can report what they *actually loaded*.

## 7) Closing: the decision tree (4:50–end)
- “curl first (control the network), then browser cache, then service worker.”

### Screenshot-able diagnosis tree
```
Start: “I still see the old version.”

1) curl (identity) shows OLD bytes?
   -> YES: server/CDN/origin still serving old (fix deploy/propagation)
   -> NO: curl shows NEW bytes

2) Browser (DevTools disable-cache) still shows OLD?
   -> YES: browser HTTP cache / caching headers issue (inspect headers)
   -> NO: browser shows NEW bytes

3) Page/UI still behaves like OLD?
   -> YES: likely service worker (controller) or app-level cache (check SW)
   -> NO: you’re actually on the new version
```
