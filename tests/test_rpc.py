import unittest
import sys
import os
import threading
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpc_core.rpc_server import RPCServer
from rpc_core.rpc_client import RPCClient
from rpc_core.protocol import RPCError, RPCErrorCodes

# Dummy service methods
def add(a, b):
    return a + b

def slow_method():
    time.sleep(2)
    return "done"

class TestRPCProtocol(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = '127.0.0.1'
        cls.port = 8888
        cls.server = RPCServer(cls.host, cls.port)
        
        # Register methods
        cls.server.register_function(add)
        cls.server.register_function(slow_method)
        
        # Run server in a background thread
        cls.server_thread = threading.Thread(target=cls.server.start, daemon=True)
        cls.server_thread.start()
        
        # Give server time to start listening
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def setUp(self):
        self.client = RPCClient(self.host, self.port)
        self.client.connect()

    def tearDown(self):
        self.client.disconnect()

    def test_successful_call(self):
        result = self.client.call("add", 5, 3)
        self.assertEqual(result, 8)

    def test_method_not_found(self):
        with self.assertRaises(RPCError) as context:
            self.client.call("subtract", 5, 3)
        
        self.assertEqual(context.exception.code, RPCErrorCodes.METHOD_NOT_FOUND)

    def test_invalid_params(self):
        with self.assertRaises(RPCError) as context:
            # "add" takes 2 arguments, we provide 1
            self.client.call("add", 5)
        
        self.assertEqual(context.exception.code, RPCErrorCodes.INVALID_PARAMS)

    def test_timeout(self):
        with self.assertRaises(RPCError) as context:
            # Server sleeps for 2 seconds, we wait for 1 second
            self.client.call("slow_method", timeout=1.0)
            
        self.assertEqual(context.exception.code, RPCErrorCodes.TIMEOUT)

if __name__ == '__main__':
    unittest.main()
