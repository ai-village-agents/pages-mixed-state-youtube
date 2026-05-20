# Video 7 — narration (draft)

## Slide 1 — Service worker: the cache you forgot
If you’ve ever had a deploy where the *same URL* shows two different versions…

Sometimes it’s not your CDN cache.
Sometimes it’s not your browser HTTP cache.

Sometimes it’s a **service worker**.

## Slide 2 — Why this matters
This is the kind of bug that burns hours.

One device sees the fix.
Another device still sees an older version.

The fastest way out is to stop guessing and start isolating variables.

## Slide 3 — What a service worker can do
A service worker can sit between your page and the network.

Inside its scope, it can intercept requests and respond from a cache it controls.

That can be great for offline support — and confusing when your deploy changes.

## Slide 4 — How “two versions” happen
Here’s a common split:

Browser A has a service worker installed and controlling the page.
Browser B doesn’t — or it has a newer one.

Now “same URL” doesn’t mean “same code path”.

## Slide 5 — First proof: is SW in the path?
First, prove whether a service worker is involved.

In DevTools, look for an indicator like “from ServiceWorker” on the request.
Exact wording varies by browser.

And in the Console, check whether the page is controlled.
For example, run `navigator.serviceWorker.controller` — if it’s non-null, a service worker is controlling this page.

## Slide 6 — CLI vs browser (important)
This is an easy trap:

`curl` can show you the *network* response…
while your browser is being served by a service worker.

So when `curl` and the browser disagree, don’t panic.
Treat it as a strong clue.

## Slide 7 — Isolate the variable
Now isolate.

Try a private window — it often starts with less service-worker state.

If you have access, unregister the service worker and hard reload.
And if your DevTools supports it, use a “bypass service worker” setting.

## Slide 8 — Compare variants
Compare on purpose.

Browser with a service worker controlling the page versus a browser without.
Device A versus device B.

Same URL, different controller state — that’s your smoking gun.

## Slide 9 — Fix patterns (safer defaults)
The fix depends on your app, but a few patterns help:

Make sure your service-worker script can actually update.
Serving `sw.js` with `Cache-Control: no-cache` (or versioning its URL) helps avoid “stuck on old SW” behavior.

Keep your HTML shell fresher than your hashed assets.
And cache hashed assets aggressively.

## Slide 10 — Recap checklist
Recap:

One: prove whether a service worker is in the path.

Two: isolate by bypassing or unregistering.

Three: re-test, then document the exact before-and-after.

Proof beats superstition.
