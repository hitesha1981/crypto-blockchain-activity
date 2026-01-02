import json
from datetime import datetime, UTC
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

with open("dashboards/metrics.json") as f:
    m = json.load(f)

chains = m["chains"]

# 1. Update Table
rows = []
for c in chains:
    fee = c.get("avg_fee", "N/A")
    # For BTC it is sat/vbyte, for ETH it is Gwei. Let's format it.
    if c["chain"] == "Bitcoin" and isinstance(fee, (int, float)):
        fee_str = f"{fee:.1f} sat/vb"
    elif c["chain"] == "Ethereum" and isinstance(fee, (int, float)):
        fee_str = f"{fee:.1f} Gwei"
    else:
        fee_str = str(fee)

    tps = c.get("tps", 0)
    util = c.get("utilization", 0)
    
    rows.append(f"| {c['chain']} | {c['block_height']} | {c['tx_count']} | {tps} | {util}% | {fee_str} |")

table = "\n".join([
    "| Chain | Block Height | TX Count | TPS (10 blk avg) | Block Util | Avg Fee |",
    "|------|-------------|----------|------------------|------------|---------|",
    *rows
])

Path("dashboards").mkdir(exist_ok=True)

# 2. Charts
# We want to create side-by-side charts for comparisons or individual charts?
# Let's create:
# - TPS Trend (Line)
# - Fee Price Trend (Line)
# - Block Utilization (Bar)

# TPS Trend
plt.figure(figsize=(10, 5))
for c in chains:
    history = c.get("history", [])
    if not history: continue
    
    # Sort by height just in case
    history = sorted(history, key=lambda x: x["height"])
    
    heights = [h["height"] for h in history]
    tps_vals = [h["tps"] for h in history]
    
    # Normalize heights to 0..9 for overlay plotting? Or just plot separate lines?
    # Overlaying different chains with different block heights is tricky on x-axis.
    # We can plot them as "Blocks ago" (0 to -9)
    x_axis = range(len(history))
    plt.plot(x_axis, tps_vals, marker='o', label=c["chain"])

plt.title("TPS Trend (Last 10 Blocks)")
plt.xlabel("Blocks Ago (0 = Oldest, 9 = Latest)")
plt.ylabel("Transactions Per Second")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("dashboards/tps_trend.png")
plt.close()

# TX Count Trend (Replaces simple Bar Chart)
plt.figure(figsize=(10, 5))
for c in chains:
    history = c.get("history", [])
    if not history: continue
    
    # Sort by height just in case
    history = sorted(history, key=lambda x: x["height"])
    
    vals = [h["tx_count"] for h in history]
    plt.plot(range(len(history)), vals, marker='*', linestyle='--', label=c["chain"])

plt.title("TX Count Trend (Last 10 Blocks)")
plt.xlabel("Blocks Ago")
plt.ylabel("Transactions per block")
plt.legend()
plt.grid(True, alpha=0.3)
# Keep original filename for compatibility/request
plt.savefig("dashboards/tx_per_block.png")
plt.close()

# Fee Trend
plt.figure(figsize=(10, 5))
ax1 = plt.gca()
ax2 = ax1.twinx() # Use secondary axis for different units (sat/vb vs Gwei)

colors = {"Bitcoin": "orange", "Ethereum": "blue"}

for c in chains:
    history = c.get("history", [])
    if not history: continue
    
    # Fees
    # BTC: avg_fee_sat_vbyte
    # ETH: base_fee_gwei
    if c["chain"] == "Bitcoin":
        vals = [h.get("avg_fee_sat_vbyte", 0) for h in history]
        ax1.plot(range(len(history)), vals, marker='s', color=colors["Bitcoin"], label="Bitcoin (sat/vb)")
    elif c["chain"] == "Ethereum":
        vals = [h.get("base_fee_gwei", 0) for h in history]
        ax2.plot(range(len(history)), vals, marker='^', color=colors["Ethereum"], label="Ethereum (Gwei)")

ax1.set_xlabel("Blocks Ago")
ax1.set_ylabel("Bitcoin Fee (sat/vbyte)", color=colors["Bitcoin"])
ax2.set_ylabel("Ethereum Base Fee (Gwei)", color=colors["Ethereum"])

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=0)

plt.title("Fee Trend (Last 10 Blocks)")
plt.grid(True, alpha=0.3)
plt.savefig("dashboards/fee_trend.png")
plt.close()


# Whale Alerts
whales = []
for c in chains:
    for w in c.get("whales", []):
        if c["chain"] == "Ethereum":
            whales.append(f"- Ethereum | {w['value_eth']} ETH | `{w['hash'][:12]}…`")
        elif c["chain"] == "Bitcoin":
            whales.append(f"- Bitcoin | {w['value_btc']} BTC | `{w['txid'][:12]}…`")

if not whales:
    whales.append("No whale-sized transfers detected in latest blocks.")

# 3. Render Template
with open("README.template.md") as f:
    r = f.read()

r = r.replace("{{TIME}}", datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC"))
r = r.replace("{{USED}}", str(m["api_usage"]["used"]))
r = r.replace("{{TABLE}}", table)
r = r.replace("{{WHALES}}", "\n".join(whales))

with open("README.md", "w") as f:
    f.write(r)

print("README.md rendered")