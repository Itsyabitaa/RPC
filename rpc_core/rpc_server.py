import sys
import os
import traceback

from rpc_core.transport import RPCServerTransport
from rpc_core.serializer import JSONSerializer, DeserializationError, SerializationError
from rpc_core.protocol import RPCErrorCodes

class RPCServer:
    def __init__(self, host: str, port: int):
        self.transport = RPCServerTransport(host, port, self._dispatch)
        self.methods = {}

    def register_function(self, func, name=None):
        """
        Registers a function to be callable via RPC.
        """
        method_name = name if name else func.__name__
        self.methods[method_name] = func
        print(f"[*] Registered RPC method: {method_name}")

    def start(self):
        self.transport.start()

    def stop(self):
        self.transport.stop()

    def _dispatch(self, data: bytes) -> bytes:
        """
        Unmarshals the request, routes it to the correct function,
        and marshals the response.
        """
        request_id = None
        try:
            # 1. Unmarshal
            request = JSONSerializer.deserialize(data)
            request_id = request.get("request_id")
            method_name = request.get("method")
            params = request.get("params", [])

            if not method_name:
                return self._create_error_response(request_id, RPCErrorCodes.INVALID_PARAMS, "Method name is missing.")

            # 2. Lookup Method
            if method_name not in self.methods:
                return self._create_error_response(request_id, RPCErrorCodes.METHOD_NOT_FOUND, f"Method '{method_name}' not found.")

            func = self.methods[method_name]

            # 3. Execute Method
            try:
                result = func(*params)
                return self._create_success_response(request_id, result)
            except TypeError as e:
                # Invalid parameters passed to the function
                return self._create_error_response(request_id, RPCErrorCodes.INVALID_PARAMS, f"Invalid parameters for '{method_name}': {e}")
            except Exception as e:
                # Internal execution error
                traceback.print_exc()
                return self._create_error_response(request_id, RPCErrorCodes.INTERNAL_ERROR, f"Internal error during execution: {e}")

        except DeserializationError as e:
            return self._create_error_response(request_id, RPCErrorCodes.PARSE_ERROR, str(e))
        except Exception as e:
            return self._create_error_response(request_id, RPCErrorCodes.INTERNAL_ERROR, str(e))

    def _create_success_response(self, request_id, result) -> bytes:
        response = {
            "request_id": request_id,
            "result": result,
            "error": None
        }
        return JSONSerializer.serialize(response)

    def _create_error_response(self, request_id, code: int, message: str) -> bytes:
        response = {
            "request_id": request_id,
            "result": None,
            "error": {
                "code": code,
                "message": message
            }
        }
        # Fallback to plain json if serialization fails to avoid infinite loops
        try:
            return JSONSerializer.serialize(response)
        except Exception:
            import json
            return json.dumps(response).encode('utf-8')
