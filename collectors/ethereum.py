from collectors.common import RPCClient, calculate_tps

WHALE_THRESHOLD_ETH = 5000

def collect(endpoint, counter, chain="Ethereum"):
    rpc = RPCClient(endpoint, counter)
    
    # 1. Get current height
    bh_hex = rpc.call("eth_blockNumber")
    current_height = int(bh_hex, 16)
    
    history = []
    prev_time = None
    
    # History window: 10 blocks
    for h in range(current_height - 9, current_height + 1):
        try:
            is_latest = (h == current_height)
            # Full transaction objects only needed for latest block (whale detection) - Hitesh
            block = rpc.call("eth_getBlockByNumber", [hex(h), is_latest])
            
            timestamp = int(block["timestamp"], 16)
            txs = block["transactions"]
            tx_count = len(txs)
            
            tps = 0.0
            if prev_time:
                tps = calculate_tps(tx_count, timestamp - prev_time)
            prev_time = timestamp
            
            gas_used = int(block["gasUsed"], 16)
            gas_limit = int(block["gasLimit"], 16)
            utilization = round((gas_used / gas_limit) * 100, 2)
            
            base_fee = 0.0
            if "baseFeePerGas" in block:
                base_fee = int(block["baseFeePerGas"], 16) / 1e9
            
            history.append({
                "height": h,
                "tx_count": tx_count,
                "base_fee_gwei": round(base_fee, 2),
                "tps": tps,
                "utilization": utilization,
                "timestamp": timestamp
            })
            
            if is_latest:
                for tx in txs:
                    val = int(tx.get("value", "0x0"), 16) / 1e18
                    if val >= WHALE_THRESHOLD_ETH:
                        whales.append({
                            "hash": tx["hash"],
                            "value_eth": round(val, 2)
                        })
        
        except Exception as e:
            print(f"Block fetch failed {h}: {e}")
            continue

    latest_stats = history[-1] if history else {}

    return {
        "chain": chain,
        "block_height": current_height,
        "tx_count": latest_stats.get("tx_count", 0),
        "avg_fee": latest_stats.get("base_fee_gwei", 0), # Using base fee now
        "tps": latest_stats.get("tps", 0),
        "utilization": latest_stats.get("utilization", 0),
        "whales": whales[:5] if 'whales' in locals() else [],
        "history": history
    }