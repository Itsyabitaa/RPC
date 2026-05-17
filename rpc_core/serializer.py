import json

class SerializationError(Exception):
    pass

class DeserializationError(Exception):
    pass

class JSONSerializer:
    """
    Handles marshaling and unmarshaling of RPC messages.
    Supports only int, str, and list (arrays) for parameters and results.
    """
    
    @staticmethod
    def _validate_value(val):
        """
        Recursively checks that the value only contains supported types.
        Supported types: int, str, list, None (for null/empty results)
        """
        if val is None:
            return True
        elif isinstance(val, bool):
            # In Python bool is a subclass of int, so we explicitly deny it
            # if we strictly want only int, str, and arrays.
            # But usually bool is fine. The spec says int, string, arrays. Let's strict check.
            raise SerializationError(f"Unsupported data type: bool ({val})")
        elif isinstance(val, int):
            return True
        elif isinstance(val, str):
            return True
        elif isinstance(val, list):
            for item in val:
                JSONSerializer._validate_value(item)
            return True
        else:
            raise SerializationError(f"Unsupported data type: {type(val).__name__} ({val})")

    @staticmethod
    def serialize(obj: dict) -> bytes:
        """
        Validates the object types and serializes it to a JSON byte string.
        """
        try:
            # Validate the structure based on if it's a request or response
            if not isinstance(obj, dict):
                raise SerializationError("Top-level object must be a dictionary.")
            
            # Check fields
            if "method" in obj:
                # It's a request
                JSONSerializer._validate_value(obj.get("request_id"))
                JSONSerializer._validate_value(obj.get("method"))
                params = obj.get("params", [])
                if not isinstance(params, list):
                    raise SerializationError("Params must be an array (list).")
                JSONSerializer._validate_value(params)
            elif "result" in obj or "error" in obj:
                # It's a response
                JSONSerializer._validate_value(obj.get("request_id"))
                JSONSerializer._validate_value(obj.get("result"))
                JSONSerializer._validate_value(obj.get("error"))
            else:
                raise SerializationError("Malformed RPC message format.")

            json_str = json.dumps(obj)
            return json_str.encode('utf-8')
            
        except Exception as e:
            if isinstance(e, SerializationError):
                raise e
            raise SerializationError(f"Failed to serialize object: {e}")

    @staticmethod
    def deserialize(data: bytes) -> dict:
        """
        Deserializes a JSON byte string back to a Python dictionary.
        """
        if not data:
            raise DeserializationError("Empty data received.")
            
        try:
            json_str = data.decode('utf-8')
            obj = json.loads(json_str)
            
            if not isinstance(obj, dict):
                raise DeserializationError("Deserialized data is not a dictionary.")
                
            return obj
        except json.JSONDecodeError as e:
            raise DeserializationError(f"Invalid JSON format: {e}")
        except UnicodeDecodeError as e:
            raise DeserializationError(f"Invalid encoding, expected UTF-8: {e}")
        except Exception as e:
            raise DeserializationError(f"Failed to deserialize data: {e}")
