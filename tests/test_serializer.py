import unittest
import sys
import os

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpc_core.serializer import JSONSerializer, SerializationError, DeserializationError

class TestJSONSerializer(unittest.TestCase):
    
    def test_serialize_valid_request(self):
        req = {
            "request_id": 1,
            "method": "add",
            "params": [5, "ten", [1, 2]]
        }
        data = JSONSerializer.serialize(req)
        self.assertIsInstance(data, bytes)
        self.assertTrue(b'"method": "add"' in data)
        
    def test_deserialize_valid_request(self):
        data = b'{"request_id": 1, "method": "add", "params": [5, "ten", [1, 2]]}'
        obj = JSONSerializer.deserialize(data)
        self.assertEqual(obj["request_id"], 1)
        self.assertEqual(obj["method"], "add")
        self.assertEqual(obj["params"], [5, "ten", [1, 2]])
        
    def test_serialize_valid_response(self):
        resp = {
            "request_id": 1,
            "result": 15,
            "error": None
        }
        data = JSONSerializer.serialize(resp)
        self.assertIsInstance(data, bytes)
        self.assertTrue(b'"result": 15' in data)

    def test_serialize_invalid_type_float(self):
        req = {
            "request_id": 1,
            "method": "add",
            "params": [5.5, 3] # Float is not supported
        }
        with self.assertRaises(SerializationError):
            JSONSerializer.serialize(req)

    def test_serialize_invalid_type_dict_in_params(self):
        req = {
            "request_id": 1,
            "method": "add",
            "params": [{"key": "value"}] # Dict is not supported in params
        }
        with self.assertRaises(SerializationError):
            JSONSerializer.serialize(req)

    def test_serialize_invalid_type_bool(self):
        req = {
            "request_id": 1,
            "method": "check",
            "params": [True] # Bool explicitly disabled based on strict int/str/array rule
        }
        with self.assertRaises(SerializationError):
            JSONSerializer.serialize(req)
            
    def test_serialize_malformed_structure(self):
        req = [1, 2, 3] # Must be a dictionary at top level
        with self.assertRaises(SerializationError):
            JSONSerializer.serialize(req)
            
    def test_deserialize_malformed_json(self):
        data = b'{"request_id": 1, "method": "add", "params": [5, 3' # Missing closing brackets
        with self.assertRaises(DeserializationError):
            JSONSerializer.deserialize(data)

if __name__ == '__main__':
    unittest.main()
