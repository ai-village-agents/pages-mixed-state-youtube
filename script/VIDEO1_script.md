Video description: A calm, evidence-first explainer about why two people can see different versions of the same GitHub Pages site, what mixed-state deployments are, and how to verify large HTML responses safely. It walks through caching, CDN behavior, asset mismatches, and practical curl techniques for range requests. Ends with a short integrity note on reporting what you observed.

Video description: We start with a relatable refresh mismatch story, then unpack temporary mixed-state causes on GitHub Pages. A checklist covers cache-busting, raw vs served content, hard refresh, and careful range requests with gzip caveats.

Video description: The video includes on-screen text cues, simple diagrams, and terminal demos, guiding viewers to reproduce verification steps at home without hype.

# Two Versions of the Same Page: GitHub Pages mixed-state + how to verify huge HTML safely

**Tone note:** Calm, evidence-first, no hype.

## 00:00 Hook — the split-screen moment
- [Direction] Split-screen browser tabs; left tab shows older layout, right tab shows newer layout.
- [Narration] “I refreshed and saw the old navbar. You refreshed and saw the brand-new hero. We jumped to conclusions: ‘Deployment is broken!’”
- [On-screen text] “Same URL, different page?”
- [Narration] “Then we realized both could be true for a few minutes. This is a classic mixed-state deployment.”

## 00:40 What “mixed-state” means on GitHub Pages
- [Direction] Simple diagram: origin → CDN edges → viewers.
- [Narration] “Mixed-state is when parts of a site update at different times. GitHub Pages uses a CDN, so edges can briefly serve different versions.”
- [On-screen text] “Temporary | CDN edges | cached assets”
- [Narration] “You might see: HTML from the new build, CSS from the old build, or vice versa.”

## 01:20 Causes (without overclaiming)
- [Direction] Bullet list appears one by one.
- [Narration] “Common, temporary causes include:”
- [On-screen text] “Edge cache propagation”
- [Narration] “1) CDN edge caches propagating at different speeds.”
- [On-screen text] “Asset version mismatch”
- [Narration] “2) Asset version mismatch—HTML points to CSS/JS still cached at old URLs when hashes aren’t updated.”
- [On-screen text] “Service worker?”
- [Narration] “3) A service worker or aggressive cache headers keeping old files locally.”
- [On-screen text] “Gzip + Range”
- [Narration] “4) Large, gzipped HTML served with Range support; partial fetches can look inconsistent if decoded mid-stream.”
- [Narration] “All of these are temporary; they settle once caches align or you fetch a fresh copy.”

## 02:20 Quick sanity checks before panicking
- [Direction] On-screen checklist overlay.
- [Narration] “Step zero: don’t assume malice. Assume caching.”
- [On-screen text] “Try in order”
- [Narration] “Try a hard refresh: Ctrl+Shift+R or Cmd+Shift+R.”
- [Narration] “Open a private window to skip some cached entries.”
- [Narration] “If it’s still weird, add a cache-busting query like `?v=now`.”
- [On-screen text] “Example: https://user.github.io/site/?v=now”
- [Narration] “If that fixes it, it was local caching.”

## 03:10 Compare served site vs raw source
- [Direction] Browser devtools network tab; split with raw GitHub view.
- [Narration] “Next, compare the served site with the raw source.”
- [On-screen text] “raw.githubusercontent.com vs CDN”
- [Narration] “Open the same file on `raw.githubusercontent.com`—that bypasses the Pages CDN styling and caching.”
- [Narration] “If raw shows the new content but the site doesn’t, the CDN edge is behind.”
- [Narration] “If both are old, the repository content didn’t publish yet.”

## 04:00 Inspect headers to confirm caching
- [Direction] Terminal view running curl.
- [Narration] “Use curl to see cache headers.”
- [On-screen text] “`curl -I https://user.github.io/site/`”
- [Narration] “Look at `Age`, `Cache-Control`, and `ETag`. A high Age suggests you’re seeing a cached response.”

## 04:40 Handling huge HTML files safely
- [Direction] Terminal zoom-in; showing large file size message.
- [Narration] “Some sites have a massive pre-rendered HTML. Fetching it naively can be slow.”
- [On-screen text] “Use HTTP Range”
- [Narration] “Use HTTP Range requests to grab just the head and tail without decompressing mid-stream.”
- [On-screen text] “Commands”
- [Narration] “First, avoid gzip when doing ranges:”
- [On-screen text] ``curl -H "Accept-Encoding: identity" -I https://user.github.io/site/``
- [Narration] “Then fetch the first 4 KB to confirm the top of the document:”
- [On-screen text] ``curl -H "Accept-Encoding: identity" -r 0-4095 https://user.github.io/site/``
- [Narration] “Grab the last 4 KB to spot footers or version stamps:”
- [On-screen text] ``curl -H "Accept-Encoding: identity" -r -4096 https://user.github.io/site/``

## 05:50 Why gzip + Range can mislead
- [Direction] Simple graphic: compressed block vs byte ranges.
- [Narration] “If you request compressed content and a byte range, the server may slice the compressed stream, not the decoded HTML.”
- [Narration] “The bytes you see may not map cleanly to characters, and you can misread version strings.”
- [On-screen text] “Avoid gzip for Range”
- [Narration] “That’s why we set `Accept-Encoding: identity` before using ranges.”

## 06:40 Practical verification checklist
- [Direction] Checklist with checkmarks appearing.
- [Narration] “Put it together with this quick checklist:”
- [On-screen text] “1) Hard refresh”
- [Narration] “1) Hard refresh in normal and private windows.”
- [On-screen text] “2) Cache-bust ?v=now”
- [Narration] “2) Add `?v=now` to bust local caches.”
- [On-screen text] “3) Compare raw vs CDN”
- [Narration] “3) Compare `raw.githubusercontent.com` to the live site.”
- [On-screen text] “4) Check headers”
- [Narration] “4) `curl -I` to inspect `Age` and `Cache-Control`.”
- [On-screen text] “5) Range with identity”
- [Narration] “5) For huge pages, use `Accept-Encoding: identity` with ranges to check top and bottom quickly.”
- [On-screen text] “6) Re-check after 5–10 minutes”
- [Narration] “6) Wait a few minutes and retry; CDN propagation is often minutes, not hours.”

## 08:00 Ethics and integrity in reports
- [Direction] Presenter to camera; calm tone.
- [Narration] “When you report a mismatch, be precise about what you observed.”
- [On-screen text] “Say: ‘From my network at 14:03 UTC’”
- [Narration] “Say ‘From my environment at 14:03 UTC, I saw version X.’”
- [Narration] “If someone else claims Y, write ‘User B reported Y; I haven’t reproduced it.’”
- [Narration] “This keeps the conversation factual and avoids blaming before evidence.”

## 09:00 Optional context: learned in public
- [Direction] Brief note with footer citation.
- [Narration] “These habits come from a public multi-agent research project where we compared notes on web anomalies.”
- [Narration] “You can adopt the same posture: test, document, and stay curious.”

## 09:40 Closing and reminder
- [Direction] Return to split-screen; now both tabs show the same version.
- [Narration] “A mixed-state GitHub Pages deployment is usually a brief cache hiccup.”
- [On-screen text] “Refresh + verify + report clearly”
- [Narration] “Use the checklist, verify with curl, and report with integrity.”
- [Narration] “If this helped, share it with someone who’s ever said, ‘It works on my machine.’”

## 10:20 Links / resources
- GitHub Pages docs: https://docs.github.com/pages
- HTTP Range requests explainer: https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests
- curl documentation: https://curl.se/docs/
