# VIDEO5 production notes (Cache-Control in the Wild)
- Target pacing: ~150 wpm, total 5–7 minutes (~0:00–7:00). Keep narration crisp; let terminal pauses breathe.

| Segment | Target timestamp (rough) | Slide # / terminal capture | Highlight on screen |
| --- | --- | --- | --- |
| Hook & promise | 0:00–0:20 | Slide 1 | Show the `Cache-Control: max-age=300, s-maxage=30, stale-while-revalidate=120` snippet; call out “which cache lied?” |
| Two-cache model | 0:20–1:00 | Slide 2 | Emphasize “browser cache vs shared cache”; underline “governs reuse windows, not deploys.” |
| Plain-language directives | 1:00–1:50 | Slide 3 | Bold the directive names (max-age, s-maxage, must-revalidate, stale-while-revalidate, no-cache) as you summarize. |
| Divergence example | 1:50–2:30 | Slide 4 | Highlight “s-maxage 30s vs max-age 300s” and the Age callout; gesture to browser vs CDN arrows. |
| Diagram | 2:30–3:00 | Slide 5 | Trace flow: Browser → CDN/edge → Origin; point at Cache-Control + Age coming back. |
| Demo intro | 3:00–3:20 | Slide 6 | Briefly show the command list; stress that curl bypasses browser cache. |
| Curl baseline headers | 3:20–3:50 | Terminal capture | Run `curl -I https://example.com/page.html`; zoom on Cache-Control, Age, CDN hint. |
| Curl forced revalidation | 3:50–4:20 | Terminal capture | Run `curl -I -H 'Cache-Control: no-cache' https://example.com/page.html`; circle changed Age/status. |
| Curl post-expiry probe | 4:20–4:50 | Terminal capture | After short wait past s-maxage/max-age, rerun `curl -I https://example.com/page.html`; watch Age reset or revalidate header. |
| Curl SWR probe | 4:50–5:30 | Terminal capture | Run `curl -I https://example.com/page.html && sleep 1 && curl -I https://example.com/page.html`; overlay tiny “typical, not guaranteed” label near stale serve to make the distinction visual. |
| Common traps | 5:30–5:50 | Slide 7 | Call out “no-cache ≠ no storage” and optional nature of SWR/must-revalidate enforcement. |
| Practical patterns | 5:50–6:20 | Slide 8 | Flash the three patterns (HTML short, assets long, sensitive no-store); show one header line each. |
| When model breaks | 6:20–6:40 | Slide 9 | Note service workers/layered CDNs; quick mention only. |
| Recap checklist | 6:40–7:00 | Slide 10 | Show checklist; remind to log URL/time/status/Cache-Control/Age/validators/CDN hints. |

## Curl commands to record (exact from VIDEO5_youtube_description.md)
- Baseline headers (segment: Curl baseline headers):  
  ```bash
  curl -I https://example.com/page.html
  ```
- Force revalidation probe (segment: Curl forced revalidation):  
  ```bash
  curl -I -H 'Cache-Control: no-cache' https://example.com/page.html
  ```
- Post-expiry probe after wait (segment: Curl post-expiry probe; wait past max-age/s-maxage before running):  
  ```bash
  # wait past max-age/s-maxage, then:
  curl -I https://example.com/page.html
  ```
- Stale-while-revalidate probe (segment: Curl SWR probe):  
  ```bash
  # SWR probe: prime then re-hit quickly
  curl -I https://example.com/page.html && sleep 1 && curl -I https://example.com/page.html
  ```

## Screen capture checklist
- Terminal font size large enough for 1080p readability; avoid semi-transparent backgrounds; keep prompt short.
- Window size: single column terminal + small camera bubble if used; no overlapping panels.
- Verify URL visible (`https://example.com/page.html` placeholder or your staging URL); no private hostnames.
- Scrub tokens/credentials from env, prompt, history; avoid showing kube contexts or git remotes if sensitive.
- For timing demos, let Age headers render fully; pause briefly after each command so values are readable.
- If using overlays, add a small on-screen “typical, not guaranteed” label during SWR demo to reinforce expectations.
