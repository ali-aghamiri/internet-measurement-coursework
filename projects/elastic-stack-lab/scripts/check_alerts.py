"""Wait for synthetic EVE alerts to appear in the local Elasticsearch index."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


QUERY = {"query": {"match": {"event_type": "alert"}}, "size": 100}


def fetch_alerts(base_url: str) -> tuple[int, Counter[str]]:
    request = Request(
        f"{base_url.rstrip('/')}/filebeat-*/_search",
        data=json.dumps(QUERY).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=5) as response:
        payload = json.load(response)
    hits = payload["hits"]
    count = hits["total"]["value"]
    sources = Counter(hit["_source"].get("src_ip", "unknown") for hit in hits["hits"])
    return count, sources


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:9200")
    parser.add_argument("--expected-alerts", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    if args.expected_alerts < 1 or args.timeout < 1:
        parser.error("expected-alerts and timeout must be positive")

    deadline = time.monotonic() + args.timeout
    last_error = "No alerts indexed yet"
    while time.monotonic() < deadline:
        try:
            count, sources = fetch_alerts(args.url)
            if count >= args.expected_alerts:
                print(f"Indexed alerts: {count}")
                for ip, number in sources.most_common():
                    print(f"  {ip}: {number}")
                return
            last_error = f"Only {count} alert(s) indexed"
        except (HTTPError, URLError, OSError, KeyError, ValueError) as error:
            last_error = str(error)
        time.sleep(2)
    parser.exit(1, f"Timed out waiting for {args.expected_alerts} alerts: {last_error}\n")


if __name__ == "__main__":
    main()
