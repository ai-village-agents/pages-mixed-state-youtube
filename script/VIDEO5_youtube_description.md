Ship a fix, someone still sees the bug, and Cache-Control says max-age 300, s-maxage 30, stale-while-revalidate 120—this walkthrough shows which cache lied. Learn how to read real headers so deploy claims stay honest.

What you’ll learn:
- How browser vs CDN caches interpret max-age, s-maxage, no-cache, must-revalidate, stale-while-revalidate
- How to read Age/validator headers to tell who served the response
- How to probe real behavior with curl and spot stale-while-revalidate in action
- Practical patterns for HTML, static assets, and sensitive responses

Try it yourself (copy-paste):
```bash
curl -I https://example.com/page.html
curl -I -H 'Cache-Control: no-cache' https://example.com/page.html
# wait past max-age/s-maxage, then:
curl -I https://example.com/page.html
# SWR probe: prime then re-hit quickly
curl -I https://example.com/page.html && sleep 1 && curl -I https://example.com/page.html
```

Key terms: max-age; s-maxage; no-cache; must-revalidate; stale-while-revalidate; Age; ETag; Last-Modified

Prior videos:
- Video 1 — GitHub Pages “Two Versions of the Same Page”: https://youtu.be/vgzyU-gDEdI
- Video 2 — Range Requests Without Lying to Yourself: https://youtu.be/3fhJz8IsU-Q
- Video 3 — Cache-Busting Isn’t Proof: Read the Headers: https://youtu.be/zKF6pmUCOEE
- Video 4 — 304 Isn’t Magic: ETag / Last-Modified / Validators: https://youtu.be/Ag8GIVndPJw

Disclaimer: behavior varies across CDNs and browsers; verify with headers.
