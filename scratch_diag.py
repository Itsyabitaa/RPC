import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpc_core.rpc_client import RPCClient
from rpc_core.serializer import JSONSerializer

client = RPCClient('127.0.0.1', 9999)
client.connect()

request_payload = {
    "request_id": "test_id",
    "method": "add",
    "params": [10, 5]
}

data = JSONSerializer.serialize(request_payload)
client.transport.set_timeout(5)
client.transport.send(data)

resp_bytes = client.transport.receive()
print(f"RAW RESP: {resp_bytes}")
resp = JSONSerializer.deserialize(resp_bytes)
print(f"PARSED RESP: {resp}")
