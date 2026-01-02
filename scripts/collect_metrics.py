import os, json
from datetime import datetime, UTC
from pathlib import Path
from collectors import ethereum, bitcoin

ETH_ENDPOINT = os.getenv("GETBLOCK_ETH_ENDPOINT")
BTC_ENDPOINT = os.getenv("GETBLOCK_BTC_ENDPOINT")

counter = {"calls": 0, "monthly_limit": 500_000}
chains = []

if ETH_ENDPOINT:
    chains.append(ethereum.collect(ETH_ENDPOINT, counter))

if BTC_ENDPOINT:
    chains.append(bitcoin.collect(BTC_ENDPOINT, counter))

if not chains:
    raise RuntimeError("No collectors enabled")

data = {
    "generated_at": datetime.now(UTC).isoformat(),
    "api_usage": {
        "used": counter["calls"],
        "remaining": counter["monthly_limit"] - counter["calls"]
    },
    "chains": chains
}

Path("dashboards").mkdir(exist_ok=True)
with open("dashboards/metrics.json", "w") as f:
    json.dump(data, f, indent=2)

print("Metrics written to dashboards/metrics.json")