# Video 8 — YouTube metadata draft

## Title
**Hard Reload Isn't Proof (Debug Caching with curl Controls)**

## Description
Hard reload clears some caches, but it isn't proof the new build shipped.  
We map a 3-layer model: CDN/server, browser HTTP cache, service worker.  
See how each layer can disagree and why a hard reload only touches part of it.  
Use curl with Accept-Encoding controls to compare identity vs compressed hashes.  
Prove the HTML entry point separately from assets before debugging further.  
Decision tree for when the CLI matches, when the browser matches, and when neither do.  
Repo root: https://github.com/ai-village-agents/pages-mixed-state-youtube  
What a proof bundle means: https://github.com/ai-village-agents/pages-mixed-state-youtube/blob/main/docs/proof_bundles_for_humans.md  
Proof bundle format: https://github.com/ai-village-agents/pages-mixed-state-youtube/blob/main/docs/publish_proof_bundle.md

## Chapters (draft)
- 0:00 Hard reload isn’t proof
- 0:21 What a hard reload really does
- 0:38 Minimal reproducible check
- 1:00 "First proof: raw fetch"
- 1:22 Compare encodings
- 1:52 Check the HTML entry point
- 2:06 Service worker vs CDN vs browser
- 2:32 Isolate state
- 2:54 Experiment matrix
- 3:14 Fix and verify
- 3:35 Decision tree (screenshot this)

## Tags (draft)
caching, hard reload, service worker, browser cache, CDN, curl, debugging, web dev, GitHub Pages
