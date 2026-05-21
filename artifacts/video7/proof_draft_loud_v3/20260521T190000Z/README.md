# Video 7 — draft loud MP4 local proof bundle (v3)

This folder captures *local* evidence about the current draft loud export:

- `ffmpeg_i.txt`: container/codec/duration info from `ffmpeg -i`.
- `loudnorm_pass_log.txt`: raw ffmpeg log from a loudnorm analysis pass.
- `loudnorm_analysis.json`: JSON extracted from the loudnorm filter output.
- `SHA256SUMS.txt`: hashes of the above files **and** the local MP4.

Notes:
- The MP4 itself is intentionally not committed (large, gitignored), but its hash is included.
- This bundle is not a publish claim; it is a reproducible local QC artifact.
