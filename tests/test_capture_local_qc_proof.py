import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]


def _generate_tiny_mp4(path: Path) -> None:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg,
        "-hide_banner",
        "-nostdin",
        "-y",
        "-f",
        "lavfi",
        "-i",
        "color=c=blue:s=160x120:r=24:d=1",
        "-f",
        "lavfi",
        "-i",
        "sine=frequency=1000:duration=1",
        "-shortest",
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-t",
        "1",
        str(path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class CaptureLocalQcProofTests(unittest.TestCase):
    def test_sha_sums_include_input_and_readme(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            input_mp4 = td_path / "tiny.mp4"
            out_dir = td_path / "bundle"

            _generate_tiny_mp4(input_mp4)

            cmd = [
                sys.executable,
                str(ROOT / "scripts" / "capture_local_qc_proof.py"),
                "--in",
                str(input_mp4),
                "--out-dir",
                str(out_dir),
            ]
            subprocess.run(cmd, check=True, cwd=ROOT)

            # Outputs exist
            self.assertTrue((out_dir / "README.md").exists())
            self.assertTrue((out_dir / "SHA256SUMS.txt").exists())
            self.assertTrue((out_dir / "ffmpeg_i.txt").exists())
            self.assertTrue((out_dir / "loudnorm_pass_log.txt").exists())

            # SHA256SUMS contains input MP4 label and README
            sums_text = (out_dir / "SHA256SUMS.txt").read_text(encoding="utf-8")
            self.assertIn("README.md", sums_text)
            self.assertIn(input_mp4.as_posix(), sums_text)


if __name__ == "__main__":
    unittest.main()
