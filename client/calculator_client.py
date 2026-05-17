import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpc_core.rpc_client import RPCClient
from rpc_core.protocol import RPCError
from client.generated_stub import CalculatorStub

def run_client():
    HOST = '127.0.0.1'
    PORT = 5555
    
    # 1. Initialize the core RPC Client
    rpc_client = RPCClient(HOST, PORT)
    
    # 2. Wrap it with the auto-generated Calculator Stub
    calculator = CalculatorStub(rpc_client)
    
    try:
        # Connect to the server
        rpc_client.connect()
        
        # --- Normal Operations ---
        print("[+] Testing addition: 10 + 5")
        res = calculator.add(10, 5)
        print(f"Result: {res}\n")
        
        print("[+] Testing subtraction: 10 - 5")
        res = calculator.subtract(10, 5)
        print(f"Result: {res}\n")
        
        print("[+] Testing multiplication: 10 * 5")
        res = calculator.multiply(10, 5)
        print(f"Result: {res}\n")
        
        print("[+] Testing division: 10 / 5")
        res = calculator.divide(10, 5)
        print(f"Result: {res}\n")
        
        # --- Exception Handling ---
        print("[+] Testing division by zero: 10 / 0")
        try:
            calculator.divide(10, 0)
        except RPCError as e:
            print(f"Caught Expected Remote Error -> Code: {e.code}, Message: {e.message}\n")
            
        print("[+] Testing invalid parameters: add('string', 5)")
        try:
            calculator.add("string", 5) # Passing a string instead of an int to cause an error
        except RPCError as e:
            print(f"Caught Expected Remote Error -> Code: {e.code}, Message: {e.message}\n")
            
    except Exception as e:
        print(f"[-] Client connection error: {e}")
    finally:
        rpc_client.disconnect()

if __name__ == "__main__":
    run_client()
