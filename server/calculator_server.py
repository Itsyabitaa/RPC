import sys
import os
import json

# Add parent directory to sys.path to allow importing from rpc_core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpc_core.transport import RPCServerTransport

def simple_handler(data: bytes) -> bytes:
    """
    A temporary handler that just echoes back the received data to prove
    that the communication layer works.
    """
    try:
        # Attempt to decode as JSON just to show we can process it
        message = json.loads(data.decode('utf-8'))
        print(f"Server received: {message}")
        
        # Create a dummy response
        response = {
            "status": "success",
            "received_message": message,
            "message": "Hello from the server!"
        }
        return json.dumps(response).encode('utf-8')
    except Exception as e:
        print(f"Error processing message: {e}")
        return json.dumps({"error": str(e)}).encode('utf-8')

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 9999
    
    server = RPCServerTransport(HOST, PORT, simple_handler)
    print("Starting temporary test server...")
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop()
