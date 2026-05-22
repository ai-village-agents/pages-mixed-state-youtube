# Video 8 — Script v0 (narration + on-screen cues)

> Working title: **Hard Reload Isn’t Proof: A Browser Cache Checklist (With curl Controls)**

## 0) Hook (0:00–0:20)
**VO:** If you’re debugging a deploy and someone says, “I hard reloaded and it’s still old,” that’s not proof.

**VO:** I’ve seen the *same symptom* come from three different places. And the fix depends on which one you’re fighting.

**On screen:** Big text: “Hard reload ≠ proof”

## 1) The 3-layer model (0:20–0:45)
**VO:** Think of it as three layers.

**VO:** One: the server or CDN—what the network returns.

**VO:** Two: the browser HTTP cache—ETags, 304s, Cache-Control.

**VO:** Three: the service worker—because it can serve responses without even hitting the network.

**On screen:** Simple 3-layer diagram. Label A/B/C.

## 2) Step 1: curl as a control (0:45–1:30)
**VO:** Step one: before we touch the browser, we get a control with curl.

**VO:** Fetch with identity encoding, save the bytes, and hash them. Now we can compare reality, not vibes.

**On screen:** Terminal snippet (from slides): identity headers + sha256.

## 3) Step 2: is the network inconsistent? (1:30–2:10)
**VO:** Repeat the curl fetch.

**VO:** If the hashes differ, you probably have server or CDN propagation—or a dynamic response you didn’t realize was changing.

**VO:** If the hashes match, the network is stable. Now we move up the stack.

**On screen:** Two hashes: match vs mismatch.

## 4) Step 3: browser HTTP cache checks (2:10–3:00)
**VO:** Next: browser cache.

**VO:** Open DevTools, go to Network, enable “Disable cache” while DevTools is open, and reload.

**VO:** Then look at the headers. Cache-Control, ETag, Age—different CDNs add different clues, but the story is in the headers.

**VO:** The important idea: hard reload is a behavior. It’s not a guarantee.

**On screen:** Network tab highlight + a few header names.

## 5) Step 4: service worker checks (3:00–4:10)
**VO:** If curl says new, and your browser network reload says new—but the app still acts old—check the service worker.

**VO:** In DevTools, Application, Service Workers: is there a controller?

**VO:** Try update, skip waiting, or unregister. Then reload and confirm the controller is gone.

**VO:** If a service worker controls the page, it can serve old bytes even when the network is new.

**On screen:** Application → Service Workers panel; “controlled by” indicator.

## 6) Prevention payoff: visible version string (4:10–4:50)
**VO:** Here’s a tiny prevention trick: put a visible version string in the UI.

**VO:** That way, when someone reports a bug, you can tell what they actually loaded.

**On screen:** Footer “build 2026-05-22.1” before/after.

## 7) Close with explicit if/then (4:50–end)
**VO:** Here’s the decision tree.

**VO:** If curl shows old: it’s server or CDN.

**VO:** If curl shows new but the browser shows old: it’s browser caching.

**VO:** If both show new but the app still looks old: it’s usually a service worker.

**VO:** Curl first. Then browser cache. Then service worker.

**On screen:** The screenshot-able decision tree slide.
