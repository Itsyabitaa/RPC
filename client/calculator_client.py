import sys
import os
import json
import time

# Add parent directory to sys.path to allow importing from rpc_core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpc_core.transport import RPCClientTransport

def run_test_client():
    HOST = '127.0.0.1'
    PORT = 9999
    
    client = RPCClientTransport(HOST, PORT)
    
    try:
        client.connect()
        
        # Test sending multiple messages to ensure framing works correctly
        for i in range(3):
            test_request = {
                "request_id": i + 1,
                "method": "ping",
                "params": [f"Message sequence {i + 1}"]
            }
            
            print(f"Sending: {test_request}")
            client.send(json.dumps(test_request).encode('utf-8'))
            
            # Wait for response
            response_bytes = client.receive()
            if response_bytes:
                response = json.loads(response_bytes.decode('utf-8'))
                print(f"Received: {response}")
            else:
                print("Server closed connection.")
                break
                
            time.sleep(0.5)
            
    except Exception as e:
        print(f"Client error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    print("Starting temporary test client...")
    run_test_client()
