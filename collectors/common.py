import requests, time

class RPCClient:
    def __init__(self, endpoint, counter):
        self.endpoint = endpoint.rstrip("/")
        self.counter = counter

    def call(self, method, params=None):
        self.counter["calls"] += 1
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": int(time.time())
        }
        headers = {"Content-Type": "application/json"}
        r = requests.post(self.endpoint, json=payload, headers=headers, timeout=15)
        if r.status_code != 200:
            raise RuntimeError(f"RPC failed {r.status_code}: {r.text}")
        return r.json()["result"]