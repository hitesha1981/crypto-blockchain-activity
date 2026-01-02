import json
from datetime import datetime, UTC
from pathlib import Path
import matplotlib.pyplot as plt

with open("dashboards/metrics.json") as f:
    m = json.load(f)

chains = m["chains"]

rows = []
for c in chains:
    fee = c["avg_fee"] if c["avg_fee"] is not None else "N/A"
    rows.append(f"| {c['chain']} | {c['block_height']} | {c['tx_count']} | {fee} |")

table = "\n".join([
    "| Chain | Block Height | TX Count | Avg Fee |",
    "|------|-------------|----------|---------|",
    *rows
])

Path("dashboards").mkdir(exist_ok=True)

labels = [c["chain"] for c in chains]
txs = [c["tx_count"] for c in chains]

plt.figure(figsize=(6,4))
plt.bar(labels, txs)
plt.title("Transactions per Latest Block")
plt.ylabel("TX count")
plt.tight_layout()
plt.savefig("dashboards/tx_per_block.png")
plt.close()

whales = []
for c in chains:
    for w in c.get("whales", []):
        if c["chain"] == "Ethereum":
            whales.append(f"- Ethereum | {w['value_eth']} ETH | `{w['hash'][:12]}…`")
        elif c["chain"] == "Bitcoin":
            whales.append(f"- Bitcoin | {w['value_btc']} BTC | `{w['txid'][:12]}…`")

if not whales:
    whales.append("No whale-sized transfers detected in latest blocks.")

with open("README.template.md") as f:
    r = f.read()

r = r.replace("{{TIME}}", datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC"))
r = r.replace("{{USED}}", str(m["api_usage"]["used"]))
# r = r.replace("{{REMAIN}}", str(m["api_usage"]["remaining"]))
r = r.replace("{{TABLE}}", table)
r = r.replace("{{WHALES}}", "\n".join(whales))

with open("README.md", "w") as f:
    f.write(r)

print("README.md rendered")