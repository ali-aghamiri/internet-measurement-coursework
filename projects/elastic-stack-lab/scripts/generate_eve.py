"""Generate synthetic Suricata-style EVE events for the Elastic lab."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path


DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "data" / "eve.json"


def build_events(start: datetime) -> list[dict]:
    if start.tzinfo is None:
        raise ValueError("start must include a timezone")
    events = []
    for i in range(20):
        events.append(
            {
                "timestamp": (start + timedelta(seconds=i)).isoformat(),
                "event_type": "flow",
                "flow_id": 10000 + i,
                "src_ip": f"198.51.100.{10 + i % 3}",
                "dest_ip": "203.0.113.10",
                "proto": "TCP",
                "app_proto": "http",
                "flow": {"bytes_toserver": 100 + 10 * i, "bytes_toclient": 400 + 20 * i},
            }
        )
    for i in range(5):
        events.append(
            {
                "timestamp": (start + timedelta(seconds=20 + i)).isoformat(),
                "event_type": "alert",
                "flow_id": 20000 + i,
                "src_ip": "192.0.2.44",
                "dest_ip": "203.0.113.10",
                "proto": "TCP",
                "alert": {
                    "action": "allowed",
                    "gid": 1,
                    "signature_id": 1000001,
                    "rev": 1,
                    "signature": "Synthetic lab: repeated suspicious connection",
                    "category": "Potentially Bad Traffic",
                    "severity": 2,
                },
            }
        )
    return events


def write_events(path: Path, start: datetime) -> int:
    events = build_events(start)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as output:
        for event in events:
            output.write(json.dumps(event, separators=(",", ":")) + "\n")
    return len(events)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    count = write_events(args.output, datetime.now(timezone.utc))
    print(f"Wrote {count} synthetic EVE events to {args.output}")


if __name__ == "__main__":
    main()
