import unittest
from unittest.mock import patch
import importlib.util
import os

# Dynamically import Python-Bridge.py as a module
spec = importlib.util.spec_from_file_location("python_bridge", os.path.join(os.path.dirname(__file__), "Python-Bridge.py"))
pb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pb)

def parse_serial_line(line):
    temp_str, hum_str = line.split(',')
    temperature = float(temp_str)
    humidity = float(hum_str)
    return temperature, humidity

class TestPythonBridge(unittest.TestCase):
    def test_parse_valid_serial_line(self):
        line = '23.5,45.2'
        temperature, humidity = parse_serial_line(line)
        self.assertEqual(temperature, 23.5)
        self.assertEqual(humidity, 45.2)

    @patch('requests.post')
    def test_post_payload(self, mock_post):
        payload = {"temperature": 22.0, "humidity": 50.0}
        mock_post.return_value.status_code = 201
        mock_post.return_value.reason = 'Created'
        response = pb.requests.post(pb.SERVER_URL, json=payload, timeout=5)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.reason, 'Created')

    def test_parse_invalid_serial_line(self):
        line = 'invalid_data'
        with self.assertRaises(ValueError):
            parse_serial_line(line)

if __name__ == '__main__':
    unittest.main() 