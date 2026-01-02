from collectors.common import RPCClient

WHALE_THRESHOLD_ETH = 5000

def collect(endpoint, counter, chain="Ethereum"):
    rpc = RPCClient(endpoint, counter)
    bh = int(rpc.call("eth_blockNumber"), 16)
    block = rpc.call("eth_getBlockByNumber", [hex(bh), True])
    txs = block["transactions"]

    fees = []
    whales = []

    for tx in txs:
        gas_price = int(tx.get("gasPrice", "0x0"), 16)
        fees.append(gas_price)

        value_eth = int(tx.get("value", "0x0"), 16) / 1e18
        if value_eth >= WHALE_THRESHOLD_ETH:
            whales.append({
                "hash": tx["hash"],
                "value_eth": round(value_eth, 2)
            })

    avg_fee = round(sum(fees)/len(fees)/1e9, 2) if fees else 0

    return {
        "chain": chain,
        "block_height": bh,
        "tx_count": len(txs),
        "avg_fee": avg_fee,
        "whales": whales[:5]
    }