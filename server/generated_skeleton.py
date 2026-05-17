# ==========================================
# AUTO-GENERATED SKELETON FILE. DO NOT MODIFY.
# ==========================================

class CalculatorSkeleton:
    def __init__(self, rpc_server, service_impl):
        self.rpc_server = rpc_server
        self.service_impl = service_impl
        self._register_methods()

    def _register_methods(self):
        self.rpc_server.register_function(self.service_impl.add, "add")
        self.rpc_server.register_function(self.service_impl.subtract, "subtract")
        self.rpc_server.register_function(self.service_impl.multiply, "multiply")
        self.rpc_server.register_function(self.service_impl.divide, "divide")
