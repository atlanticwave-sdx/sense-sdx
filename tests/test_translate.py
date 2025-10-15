import unittest
import json
from sense_sdx.translate import (
    Domaintranslator,
)  # Adjust import if function/class name differs


class TestTranslate(unittest.TestCase):
    def setUp(self):
        # Load example JSON file
        with open("./tests/data/mren8700.json", "r") as file:
            self.example_data = json.load(file)

    def test_domain_to_sdx_node_json(self):
        d_t = Domaintranslator()
        result = d_t.domain_to_sdx_node_json(self.example_data)
        print(result)
        self.assertIsNotNone(result)
        # Add more asserts based on expected output structure
        # For example, if translation adds a specific field:
        # self.assertIn('sdx_node', result)


if __name__ == "__main__":
    unittest.main()
