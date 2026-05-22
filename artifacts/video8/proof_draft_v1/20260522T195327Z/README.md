# Local QC proof bundle
This directory holds reproducible local QC artifacts for `build/video8/video8_upload_candidate_draft.mp4`. The MP4 itself is not committed; only lightweight logs and hashes are stored.
Captured files:
- README.md: this overview.
- ffmpeg_i.txt: stderr from `ffmpeg -i` (no output written).
- loudnorm_pass_log.txt: stderr from the loudnorm analysis pass.
- loudnorm_analysis.json: JSON snapshot parsed from loudnorm stderr (last object).
- SHA256SUMS.txt: sha256 of the input MP4 plus the files above.

## Loudness snapshot
Analysis targets: I=-15, TP=-1.5, LRA=11 (analysis-only, no output media).
Parsed loudnorm values are in `loudnorm_analysis.json`; full stderr is in `loudnorm_pass_log.txt`.
