304 is not magic.

If you run curl dash I and you see 304 Not Modified, that is not proof your latest deploy is everywhere.

A 304 is a claim about this request and this validator.

Two headers matter a lot.
ETag is an opaque version identifier chosen by the server.
Last Modified is a timestamp for when the resource last changed.

They are called validators because you can ask, has this changed since the version I saw.

A conditional request is you saying, give me this resource only if it does not match this ETag.
Or, only if it is newer than this Last Modified time.

If the server agrees it is unchanged, it can reply 304 with headers and no body.
If it changed, you get 200 and a body, plus a new ETag or Last Modified.

Here is the practical pattern.
First, capture the validators.
Second, send a conditional request using those validators.

This is especially helpful when the page is huge, because you can keep the payload tiny.

What does a 304 prove.
Relative to the validator you sent, the server says unchanged.

What does it not prove.
It does not prove every CDN edge has the same version.
It does not prove your deploy fully propagated.
And it does not prove other URLs or cache keys are not serving something different.

If you want to talk about mixed state, you need comparisons.
Compare different URLs and cache keys.
And for huge HTML, confirm with Range head plus tail.

Cache behavior is governed by Cache Control.
No cache does not mean do not cache.
It means you must revalidate before using it.
Max age controls how long a cache can reuse a response without revalidation.

So you can see a 304 from one place, and a stale 200 from another, depending on what each cache has and whether it revalidated.

Here is a practical checklist.
Log the URL, the time, the status, ETag or Last Modified, Age, Cache Control, and any served by hint headers like Via.

Then repeat later.

The biggest win is not a perfect model.
It is a paper trail of what you actually observed.

304 is useful.
Just treat it as evidence about a specific validator, not a global guarantee.

For a safer workflow, chain this with reading headers in Video 3, and Range head plus tail with Accept Encoding identity in Video 2.
