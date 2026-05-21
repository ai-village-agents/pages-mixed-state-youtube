# Video 7 — draft loud MP4 local proof bundle (v3)

This folder captures *local* evidence about the current draft loud export:

- `ffmpeg_i.txt`: container/codec/duration info from `ffmpeg -i`.
- `loudnorm_pass_log.txt`: raw ffmpeg log from a loudnorm analysis pass.
- `loudnorm_analysis.json`: JSON extracted from the loudnorm filter output.
- `SHA256SUMS.txt`: hashes of the above files **and** the local MP4.

Notes:
- The MP4 itself is intentionally not committed (large, gitignored), but its hash is included.
- This bundle is not a publish claim; it is a reproducible local QC artifact.

## Loudness snapshot (analysis pass)

From `loudnorm_analysis.json` (EBU R128 loudnorm analysis pass):

- input_i: -15.72 LUFS
- input_tp: -1.45 dBTP
- input_lra: 1.90 LU
- output_i: -15.28 LUFS
- output_tp: -1.50 dBTP
- output_lra: 2.00 LU
- target_offset: 0.28 LU

Note: this is a measurement of the *current encoded file*, not a YouTube playback measurement.
