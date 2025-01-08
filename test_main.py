import unittest
import json
from main import generate_pipeline

class TestMain(unittest.TestCase):
    def test_generate_pipeline(self):
        self.assertEqual(generate_pipeline(), json.dumps({"steps": [{ "command": "echo 'Hello, world!'" }]}, indent=4))

if __name__ == "__main__":
    unittest.main()
