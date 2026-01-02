from collectors.common import RPCClient

WHALE_THRESHOLD_BTC = 100  # BTC

def collect(endpoint, counter):
    rpc = RPCClient(endpoint, counter)

    info = rpc.call("getblockchaininfo")
    height = info["blocks"]

    block_hash = rpc.call("getblockhash", [height])
    block = rpc.call("getblock", [block_hash, 2])  # verbosity=2

    whales = []

    for tx in block["tx"]:
        total_out = 0.0
        for vout in tx.get("vout", []):
            total_out += vout.get("value", 0.0)

        if total_out >= WHALE_THRESHOLD_BTC:
            whales.append({
                "txid": tx["txid"],
                "value_btc": round(total_out, 2)
            })

    return {
        "chain": "Bitcoin",
        "block_height": height,
        "tx_count": len(block["tx"]),
        "avg_fee": None,
        "whales": whales[:5]
    }
