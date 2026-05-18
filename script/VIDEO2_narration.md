[SLIDE 1] Range Requests Without Lying to Yourself. Quick, practical walkthrough for huge HTML on GitHub Pages or any CDN where compression is on by default.

[SLIDE 2] Hook: you `curl -r 0-4095 https://...` and the first 4 KB looks like gibberish. We are going to show why and how to get trustworthy samples without guesswork.

[SLIDE 3] What Range really means: Range is bytes, not characters. With HTTP, Accept-Encoding influences which bytes you get. Range is bytes; if the response is gzip, you're slicing compressed bytes. That is the key idea to keep in your head as we sample.

[SLIDE 4] The pitfall: when the server sends gzip, your range is taken over the compressed stream. The slice does not map to the top or bottom of the decoded HTML, so it looks corrupted or hides the version stamp you were hoping to spot.

[SLIDE 5] Step 1: check headers before sampling. You want to see if the server supports ranges and whether it is compressing the response. Use:
```bash
curl -sI https://user.github.io/site/ | egrep -i 'accept-ranges|content-encoding|content-length'
```
If you already see `Content-Encoding: gzip`, that tells you the bytes will be compressed unless you change your request.

[SLIDE 6] Step 2: force identity so you are ranging the plain bytes. Same probe, but with an explicit header:
```bash
curl -sI -H 'Accept-Encoding: identity' https://user.github.io/site/ \
  | egrep -i 'accept-ranges|content-encoding|content-length'
```
If the encoding disappears or shows identity, you know the server honored the request and you can range readable bytes.

[SLIDE 7] Step 3: head sample once identity is confirmed. Fetch the first 4 KB:
```bash
curl -s -H 'Accept-Encoding: identity' -r 0-4095 https://user.github.io/site/
```
This should show a sane DOCTYPE, head tags, maybe a version string near the top.

[SLIDE 8] Step 4: tail sample to see the end of the file:
```bash
curl -s -H 'Accept-Encoding: identity' -r -4096 https://user.github.io/site/
```
If you are sampling a huge HTML, this is where build IDs, closing tags, or integrity metadata usually live.

[SLIDE 9] Optional verification: search both samples for version or build markers to detect split deployments quickly.
```bash
curl -s -H 'Accept-Encoding: identity' -r 0-8191  https://... | rg -n 'version|build|id:'
curl -s -H 'Accept-Encoding: identity' -r -8192 https://... | rg -n 'version|build|id:'
```
If one side has a new build ID and the other does not, you are seeing mixed state, not necessarily a bad deploy.

[SLIDE 10] Safety and recap: head/tail samples are evidence of served bytes at that time, not proof of the whole document. Log the URL, time, and headers. Range is bytes; if the response is gzip, you're slicing compressed bytes, so force identity before using byte ranges. That keeps your samples honest and stops the gibberish. Outro: link to repo and Video 1 for the broader mixed-state checklist.
