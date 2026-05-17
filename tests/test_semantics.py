import unittest
import sys
import os
import threading
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpc_core.rpc_server import RPCServer
from rpc_core.rpc_client import RPCClient

# A global execution counter to prove if a method was run more than once
execution_count = 0

def stateful_method():
    """
    Increments a counter and returns it. 
    Also artificially sleeps to easily trigger client timeouts if we want to simulate a lost response.
    """
    global execution_count
    execution_count += 1
    
    # We delay so the client times out and retries.
    # When the server finishes, the client has already closed the connection and retried.
    time.sleep(1.5)
    return f"Count is {execution_count}"


class TestSemantics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = '127.0.0.1'
        cls.port = 7777
        cls.server = RPCServer(cls.host, cls.port)
        
        cls.server.register_function(stateful_method)
        
        cls.server_thread = threading.Thread(target=cls.server.start, daemon=True)
        cls.server_thread.start()
        
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def setUp(self):
        global execution_count
        execution_count = 0
        self.client = RPCClient(self.host, self.port)
        self.client.connect()

    def tearDown(self):
        self.client.disconnect()

    def test_duplicate_detection_and_retry(self):
        """
        Tests At-Most-Once semantics.
        The client calls a method that takes 1.5 seconds but has a timeout of 0.5s.
        Client will timeout, reconnect, and retry with the SAME request_id.
        Server will eventually finish the first request, cache it, and when the
        retry arrives, it will just return the cached response without incrementing the counter again.
        """
        # Call with a 0.5s timeout. The method takes 1.5s.
        # Client will timeout twice, then on the third attempt the server will have cached the result.
        # Max retries is 3, so it should succeed.
        
        start_time = time.time()
        result = self.client.call("stateful_method", timeout=1.0, max_retries=3)
        end_time = time.time()

        # It should have returned the cached result of the *first* execution
        self.assertEqual(result, "Count is 1")
        
        # Prove it was only executed once by checking the global counter
        self.assertEqual(execution_count, 1)

if __name__ == '__main__':
    unittest.main()
