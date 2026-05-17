import threading

class ResponseCache:
    """
    Thread-safe cache for tracking processed request IDs to prevent
    duplicate execution in At-Most-Once / Exactly-Once semantics.
    """
    def __init__(self):
        self.cache = {}
        self.lock = threading.Lock()

    def get(self, request_id):
        with self.lock:
            return self.cache.get(request_id)

    def set(self, request_id, response_bytes: bytes):
        with self.lock:
            self.cache[request_id] = response_bytes
