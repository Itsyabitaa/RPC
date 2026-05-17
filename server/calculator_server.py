import sys
import os

# Ensure the parent directory is in the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpc_core.rpc_server import RPCServer
from server.services.calculator_service import CalculatorService
from server.generated_skeleton import CalculatorSkeleton

def run_server():
    HOST = '127.0.0.1'
    PORT = 9999
    
    # 1. Initialize the Core RPC Server
    rpc_server = RPCServer(HOST, PORT)
    
    # 2. Instantiate the actual business logic service
    calc_service = CalculatorService()
    
    # 3. Use the auto-generated skeleton to bind the service to the RPC server
    skeleton = CalculatorSkeleton(rpc_server, calc_service)
    
    # 4. Start serving requests
    print("Starting Calculator RPC Server...")
    try:
        rpc_server.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        rpc_server.stop()

if __name__ == "__main__":
    run_server()
