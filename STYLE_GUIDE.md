# STYLE GUIDE — VERIFICATION/DEBUGGING VIDEOS

## 1) Audience + Promise
Practical engineers who troubleshoot web delivery (CDN/browser/origin) and want fast, reproducible fixes; promise: give a runnable mental model, then prove it with live evidence so they can repeat it on their own stack.

## 2) Structure Template
- Hook: surface the pain (broken cache, stale asset, mystery 304) with a crisp symptom log.
- Model: 1–2 slides defining actors (browser ↔ CDN ↔ origin) and the specific invariant under test.
- Demo/Proof: terminal + headers on-screen; show the command, then the response; highlight the field that proves the point.
- Traps: list 2–4 likely misreads (e.g., Age vs Date, cache keys, Accept-Encoding surprises).
- Checklist: close with a repeatable set of steps the viewer can run (copy/paste ready).

## 3) Claims Discipline
- Label scope: say `typical` vs `guaranteed`; call out vendor/version when relevant.
- Prefer showing headers/commands instead of paraphrasing; keep the terminal visible.
- Log observations verbatim before explaining (e.g., “Response Age=0, Cache-Control: max-age=600”).

## 4) Visual Rules
- Slide density: max 5 bullets/slide; keep font ≥28pt; one code/headers block per slide.
- Motion cadence: small reveal every ~8–12s (bullet, highlight, or terminal scroll); avoid jump cuts during proof.
- Diagram conventions: boxes for Browser/CDN/Origin; solid arrows for request, dashed for response; label headers on arrows (Host, Cache-Control, ETag, Accept-Encoding).

## 5) Audio Rules
- Pace: target ~135–155 wpm; insert a micro-pause before each reveal so the visual lands.
- Do not read long code/headers; narrate the action and the takeaway (“curl with -H 'Accept-Encoding: identity' shows 200 with Age=0”).

## 6) End Screen + Watch Flow
- Always point to the next related video (e.g., cache invalidation follow-up); ensure Save is disabled on end screen.

## 7) Pre-Publish Checklist (10–12 items)
- Hook states the symptom and stakes.
- Model slide shows Browser/CDN/Origin boxes + arrows with header labels.
- Commands include flags for headers (`-I`, `-H`, `--compressed` when needed).
- Included `Range + Accept-Encoding: identity` edge case if relevant.
- Covered `Age semantics` (Age vs Date vs Cache-Control).
- Called out what is `typical` vs `guaranteed`.
- Terminal zoom is legible; font ≥16pt when live.
- Motion cadence: reveals every ~8–12s; no overcrowded slides.
- Audio: pace in range; micro-pauses before reveals.
- End screen points to next video; Save disabled.
- Captions/spelling verified; no long code reading.
- Checklist slide present and runnable.
