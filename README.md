# Crypto Network Reliability Dashboard

Author: Hitesh Agrawal

This repository implements an automated, on-chain reliability and activity dashboard
for major blockchain networks using direct JSON-RPC calls via GetBlock.io.

The system periodically collects low-level network signals such as:
- latest block height
- transaction throughput per block
- fee pressure indicators
- detection of unusually large (“whale”) value transfers in latest block

All data is gathered directly from blockchain RPC endpoints (no price or market APIs),
rendered into human-readable tables and charts using Python and Matplotlib, and published
as a self-updating README via GitHub Actions.

The README itself acts as the dashboard and is regenerated automatically on a schedule,
demonstrating a production-style, infrastructure-focused observability workflow rather
than a traditional UI-driven approach.

_Last updated: 2026-01-02 08:42 UTC_

## API Usage (GetBlock.io)
- Calls used: **5**

## Network Metrics
| Chain | Block Height | TX Count | Avg Fee |
|------|-------------|----------|---------|
| Ethereum | 24145822 | 399 | 0.33 |
| Bitcoin | 930552 | 3024 | N/A |

## Visuals
![Transactions](dashboards/tx_per_block.png)

## Whale Alerts (latest block)
- Transaction hashes are truncated for readability.
- Full hashes are available in `dashboards/metrics.json`
- Bitcoin | 203.4 BTC | `f256b41e67c1…`
- Bitcoin | 164.6 BTC | `71cabb366d87…`
- Bitcoin | 243.51 BTC | `bb27174a859a…`
- Bitcoin | 145.76 BTC | `65db352d3d0b…`
- Bitcoin | 195.7 BTC | `552eba2bdd92…`

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

1. GitHub Actions runs every 24 hours
2. Chain-specific collectors fetch on-chain metrics
3. API usage is counted centrally
4. Metrics are written to JSON
5. README.md is re-rendered deterministically
6. Updated dashboard is committed back to git

---