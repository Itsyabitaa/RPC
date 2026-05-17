import socket
from rpc_core.transport import RPCClientTransport
from rpc_core.serializer import JSONSerializer, DeserializationError
from rpc_core.protocol import RPCError, RPCErrorCodes

class RPCClient:
    def __init__(self, host: str, port: int):
        self.transport = RPCClientTransport(host, port)
        self.request_id_counter = 0

    def connect(self):
        self.transport.connect()

    def disconnect(self):
        self.transport.close()

    def _generate_request_id(self) -> int:
        self.request_id_counter += 1
        return self.request_id_counter

    def call(self, method_name: str, *params, timeout: float = 5.0):
        """
        Invokes a remote method synchronously with a timeout.
        """
        request_id = self._generate_request_id()
        request_payload = {
            "request_id": request_id,
            "method": method_name,
            "params": list(params)
        }

        # 1. Marshal Request
        data = JSONSerializer.serialize(request_payload)

        # 2. Set Timeout & Send
        self.transport.set_timeout(timeout)
        self.transport.send(data)

        # 3. Wait for Response
        try:
            response_data = self.transport.receive()
            if response_data is None:
                raise RPCError(RPCErrorCodes.INTERNAL_ERROR, "Server closed the connection unexpectedly.")

            # 4. Unmarshal Response
            response = JSONSerializer.deserialize(response_data)
            
            # 5. Check for Match
            if response.get("request_id") != request_id:
                raise RPCError(RPCErrorCodes.INTERNAL_ERROR, "Request ID mismatch in response.")

            # 6. Check for Error
            if response.get("error"):
                err_dict = response["error"]
                raise RPCError(err_dict.get("code", RPCErrorCodes.INTERNAL_ERROR), err_dict.get("message", "Unknown error"))

            return response.get("result")

        except socket.timeout:
            raise RPCError(RPCErrorCodes.TIMEOUT, f"Request timed out after {timeout} seconds.")
        except Exception as e:
            if isinstance(e, RPCError):
                raise e
            raise RPCError(RPCErrorCodes.INTERNAL_ERROR, f"Client error: {e}")
