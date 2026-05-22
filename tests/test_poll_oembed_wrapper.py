import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import poll_youtube_oembed_until_ready as poll  # noqa: E402


def test_poll_stops_after_ready(monkeypatch, tmp_path) -> None:
    calls: list[list[str]] = []
    exit_codes = [3, 0]

    def fake_run(cmd, **_kwargs):
        calls.append(cmd)
        rc = exit_codes.pop(0)
        stdout = "oEmbed HTTP 404; not writing" if rc == 3 else "wrote file"
        return type("Proc", (), {"returncode": rc, "stdout": stdout, "stderr": ""})()

    monkeypatch.setattr(poll.subprocess, "run", fake_run)
    monkeypatch.setattr(poll.time, "sleep", lambda _seconds: None)

    out_path = tmp_path / "out.json"
    exit_code = poll.main(
        [
            "--url",
            "https://www.youtube.com/watch?v=ABC123def",
            "--out",
            str(out_path),
            "--max-attempts",
            "5",
            "--interval",
            "0",
        ]
    )

    assert exit_code == 0
    assert len(calls) == 2
    out_idx = calls[0].index("--out")
    assert calls[0][out_idx + 1] == str(out_path)
