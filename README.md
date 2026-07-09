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

_Last updated: 2026-07-09 04:12 UTC_

## API Usage (GetBlock.io)
- Calls used: **24**

## Network Metrics
| Chain | Block Height | TX Count | TPS (10 blk avg) | Block Util | Avg Fee |
|------|-------------|----------|------------------|------------|---------|
| Ethereum | 25492551 | 180 | 15.0 | 44.44% | 0.1 Gwei |
| Bitcoin | 957259 | 5651 | 7.98 | 99.79% | N/A |

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
- Bitcoin | 110.0 BTC | `371a5ba77d56…`
- Bitcoin | 110.0 BTC | `5bcdca1673df…`
- Bitcoin | 494.97 BTC | `b05495599348…`
- Bitcoin | 143.84 BTC | `9d9d6468eaca…`
- Bitcoin | 140.71 BTC | `740d640a0c24…`

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
