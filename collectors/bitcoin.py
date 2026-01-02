from collectors.common import RPCClient, calculate_tps

WHALE_THRESHOLD_BTC = 100  # BTC

def collect(endpoint, counter):
    rpc = RPCClient(endpoint, counter)

    # 1. Get current height
    info = rpc.call("getblockchaininfo")
    height = info["blocks"]

    
    history = []
    prev_time = None
    
    # Fetch last 10 blocks
    for h in range(height - 9, height + 1):
        try:
            # max_weight is often not returned, so we use the standard segwit limit -- Hitesh 
            stats = rpc.call("getblockstats", [h, ["avgfeerate", "time", "txs", "total_weight"]])
            avg_fee = stats.get("avgfeerate", 0)
            
            tps = 0.0
            if prev_time:
                delta = stats["time"] - prev_time
                tps = calculate_tps(stats["txs"], delta)
            
            prev_time = stats["time"]
            
            MAX_WEIGHT = 4_000_000
            util = round((stats["total_weight"] / MAX_WEIGHT) * 100, 2)
            
            history.append({
                "height": h,
                "tx_count": stats["txs"],
                "avg_fee_sat_vbyte": avg_fee,
                "tps": tps,
                "utilization": util,
                "timestamp": stats["time"]
            })
            
        except Exception as e:
            print(f"Stats check failed for {h}: {e}")
            continue
            
    # Whale detection (latest block only)
    block_hash = rpc.call("getblockhash", [height])
    block = rpc.call("getblock", [block_hash, 2])
    
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

    # Summary metrics (based on latest block or average of history)
    latest_stats = history[-1] if history else {}
    
    return {
        "chain": "Bitcoin",
        "block_height": height,
        "tx_count": latest_stats.get("tx_count", len(block["tx"])),
        "avg_fee_sat_vbyte": latest_stats.get("avg_fee_sat_vbyte", 0),
        "tps": latest_stats.get("tps", 0),
        "utilization": latest_stats.get("utilization", 0),
        "whales": whales[:5],
        "history": history
    }
