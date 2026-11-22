# Crypto Network Reliability Dashboard

Author: Hitesh Agrawal (hitesha1981@gmail.com)

This repository implements an automated, on-chain reliability and activity dashboard
for major blockchain networks using direct JSON-RPC calls via GetBlock.io.

The system periodically runs every 6 hours collects low-level network signals such as:
- latest block height
- transaction throughput per block
- fee pressure indicators
- detection of unusually large (“whale”) value transfers in latest block

All data is gathered directly from blockchain RPC endpoints (no price or market APIs),
rendered into human-readable tables and charts using Python and Matplotlib, and published
as a self-updating README via GitHub Actions.

The README itself acts as the dashboard and is regenerated automatically on a 6 Hour schedule,
demonstrating a production-style, infrastructure-focused observability workflow rather
than a traditional UI-driven approach.

_Last updated: 2026-11-22 19:35 UTC_

## API Usage (GetBlock.io)
- Calls used: **24**

## Network Metrics
| Chain | Block Height | TX Count | TPS (10 blk avg) | Block Util | Avg Fee |
|------|-------------|----------|------------------|------------|---------|
| Ethereum | 26472783 | 368 | 30.67 | 58.01% | 0.1 Gwei |
| Bitcoin | 977090 | 3680 | 2.87 | 99.79% | N/A |

## Visuals
### Transactions Trend
![Transactions](dashboards/tx_per_block.png)

### TPS Trend (Last 10 Blocks)
![TPS Trend](dashboards/tps_trend.png)

### Fee Trend
![Fee Trend](dashboards/fee_trend.png)

## Whale Alerts (latest block)
- Transaction hashes are truncated for readability.
- Full hashes are available in `dashboards/metrics.json`
- Bitcoin | 106.1 BTC | `44f762a10d15…`
- Bitcoin | 250.0 BTC | `46f4396ecc84…`
- Bitcoin | 172.46 BTC | `61d9c93a8409…`
- Bitcoin | 240.83 BTC | `3cc6b2386acf…`
- Bitcoin | 125.49 BTC | `a4bfafe228d2…`

## Run locally

```bash
uv sync
export GETBLOCK_ETH_ENDPOINT=https://go.getblock.asia/REDACTED
export GETBLOCK_BTC_ENDPOINT=https://go.getblock.io/REDACTED
uv run python -m scripts.collect_metrics
uv run python -m scripts.render_readme
```
---
**Enabled (Free Tier):**
- Ethereum Mainnet
- Bitcoin Mainnet

---

## What this project demonstrates

- Production-grade RPC usage tracking
- Deterministic CI execution using `uv`
- Separation of chain-specific collectors
- Infrastructure-style observability without UI dependencies
- GitHub Actions used as a scheduler (cron)

---

## How the system works

1. GitHub Actions runs every 6 hours, 15 minute past the hour
2. Chain-specific collectors fetch on-chain metrics
3. API usage is counted centrally
4. Metrics are written to JSON
5. README.md is re-rendered deterministically
6. Updated dashboard is committed back to git

---
