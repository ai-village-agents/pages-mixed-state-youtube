import sys
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import capture_youtube_publish_proof as proof  # noqa: E402


class Sha256SumsTests(unittest.TestCase):
    def test_deterministic_order_and_content(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td)
            first = out_dir / "zeta.txt"
            second = out_dir / "alpha.txt"
            first.write_text("first\n", encoding="utf-8")
            second.write_text("second\n", encoding="utf-8")

            # Intentionally pass in unsorted order to ensure internal sorting.
            sums_path = proof.write_sha256sums(out_dir, [first, second])
            expected_lines = [
                f"{proof.sha256_file(second)}  alpha.txt\n",
                f"{proof.sha256_file(first)}  zeta.txt\n",
            ]
            self.assertEqual(sums_path.read_text().splitlines(keepends=True), expected_lines)

            # Re-run in the opposite order; output must stay identical.
            proof.write_sha256sums(out_dir, [second, first])
            self.assertEqual(sums_path.read_text().splitlines(keepends=True), expected_lines)


if __name__ == "__main__":
    unittest.main()
