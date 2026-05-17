class RPCErrorCodes:
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603
    TIMEOUT = -32000
    PARSE_ERROR = -32700

class RPCError(Exception):
    """
    Custom exception to encapsulate RPC-specific errors.
    """
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message
        }
