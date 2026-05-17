import sys
import os
import traceback

from rpc_core.transport import RPCServerTransport
from rpc_core.serializer import JSONSerializer, DeserializationError, SerializationError
from rpc_core.protocol import RPCErrorCodes
from rpc_core.semantics import ResponseCache

class RPCServer:
    def __init__(self, host: str, port: int):
        self.transport = RPCServerTransport(host, port, self._dispatch)
        self.methods = {}
        self.response_cache = ResponseCache()

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

            # 2. Check Cache for Duplicates
            if request_id:
                cached_response = self.response_cache.get(request_id)
                if cached_response is not None:
                    print(f"[*] Duplicate request {request_id} detected. Returning cached response.")
                    return cached_response

            # 3. Lookup Method
            if method_name not in self.methods:
                response = self._create_error_response(request_id, RPCErrorCodes.METHOD_NOT_FOUND, f"Method '{method_name}' not found.")
                self.response_cache.set(request_id, response)
                return response

            func = self.methods[method_name]

            # 4. Execute Method
            try:
                result = func(*params)
                response = self._create_success_response(request_id, result)
                self.response_cache.set(request_id, response)
                return response
            except TypeError as e:
                # Invalid parameters passed to the function
                response = self._create_error_response(request_id, RPCErrorCodes.INVALID_PARAMS, f"Invalid parameters for '{method_name}': {e}")
                self.response_cache.set(request_id, response)
                return response
            except Exception as e:
                # Internal execution error
                traceback.print_exc()
                response = self._create_error_response(request_id, RPCErrorCodes.INTERNAL_ERROR, f"Internal error during execution: {e}")
                self.response_cache.set(request_id, response)
                return response

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
