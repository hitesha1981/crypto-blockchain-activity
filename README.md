# Crypto Network Reliability Dashboard

Author: Hitesh Agrawal

This repository automatically tracks the top 5 gaining, top 5 losing, and top 5 highest volume cryptocurrencies in the last 24 hours using the CoinGecko API, Python, Matplotlib, and GitHub Actions updates the below content everyday at midnight.

_Last updated: 2026-01-02 06:50 UTC_

## API Usage (GetBlock.io)
- Calls used: **5**

## Network Metrics
| Chain | Block Height | TX Count | Avg Fee |
|------|-------------|----------|---------|
| Ethereum | 24145263 | 204 | 0.39 |
| Bitcoin | 930543 | 4252 | N/A |

## Visuals
![Transactions](dashboards/tx_per_block.png)

## Whale Alerts (latest block)
- Transaction hashes are truncated for readability.
- Full hashes are available in `dashboards/metrics.json`
No whale-sized transfers detected in latest blocks.

## Run locally

```bash
uv sync
export GETBLOCK_ETH_ENDPOINT=https://go.getblock.asia/REDACTED
export GETBLOCK_BTC_ENDPOINT=https://go.getblock.io/REDACTED
uv run python -m scripts.collect_metrics
uv run python -m scripts.render_readme
```