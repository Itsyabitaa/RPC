# ==========================================
# AUTO-GENERATED STUB FILE. DO NOT MODIFY.
# ==========================================

class CalculatorStub:
    def __init__(self, rpc_client):
        self.rpc_client = rpc_client

    def add(self, a, b):
        return self.rpc_client.call("add", a, b)

    def subtract(self, a, b):
        return self.rpc_client.call("subtract", a, b)

    def multiply(self, a, b):
        return self.rpc_client.call("multiply", a, b)

    def divide(self, a, b):
        return self.rpc_client.call("divide", a, b)
