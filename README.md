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

_Last updated: 2026-01-02 07:27 UTC_

## API Usage (GetBlock.io)
- Calls used: **5**

## Network Metrics
| Chain | Block Height | TX Count | Avg Fee |
|------|-------------|----------|---------|
| Ethereum | 24145449 | 335 | 0.34 |
| Bitcoin | 930544 | 3639 | N/A |

## Visuals
![Transactions](dashboards/tx_per_block.png)

## Whale Alerts (latest block)
- Transaction hashes are truncated for readability.
- Full hashes are available in `dashboards/metrics.json`
- Bitcoin | 293.85 BTC | `bad43f7d4a13…`
- Bitcoin | 185.0 BTC | `9a42bd453b0f…`
- Bitcoin | 612.56 BTC | `d347c2f0a153…`
- Bitcoin | 257.08 BTC | `5e26920d8667…`
- Bitcoin | 100.18 BTC | `1f8584888a94…`

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