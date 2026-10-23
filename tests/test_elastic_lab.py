"""Verify that the public lab fixture is safe and has searchable EVE records."""

from __future__ import annotations

from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "projects" / "elastic-stack-lab" / "scripts" / "generate_eve.py"
spec = importlib.util.spec_from_file_location("generate_eve", SCRIPT)
assert spec and spec.loader
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


def test_generated_eve_file_is_parseable_and_contains_expected_events(tmp_path: Path) -> None:
    output = tmp_path / "eve.json"
    start = datetime(2024, 4, 19, tzinfo=timezone.utc)
    assert generator.write_events(output, start) == 25
    events = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]

    assert output.stat().st_size > 1024  # Filebeat's default fingerprint threshold
    assert sum(event["event_type"] == "flow" for event in events) == 20
    alerts = [event for event in events if event["event_type"] == "alert"]
    assert len(alerts) == 5
    assert all(event["src_ip"] == "192.0.2.44" for event in alerts)
    assert all(event["alert"]["signature_id"] == 1000001 for event in alerts)
    assert all(event["timestamp"].endswith("+00:00") for event in events)
