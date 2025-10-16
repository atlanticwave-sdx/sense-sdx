import json
import unittest

from sense_sdx.translate import (  # Adjust import if function/class name differs
    Topologytranslator,
)

# Define JSON file names globally
DOMAIN_FILES = [
    "./tests/data/mren8700.json",
    "./tests/data/es.net.json",
    "./tests/data/starlight.org.json",
]


class TestTranslate(unittest.TestCase):
    def setUp(self):
        # Load example JSON file
        with open("./tests/data/es.net.json", "r") as file:
            self.example_data = json.load(file)

    def test_to_sdx_node_json(self):
        d_t = Topologytranslator()
        result = d_t.to_sdx_node_json(self.example_data)
        print(type(result))
        self.assertIsNotNone(result)
        # Add more asserts based on expected output structure
        # For example, if translation adds a specific field:
        # self.assertIn('sdx_node', result)

    def test_to_sdx_topology_json(self):
        d_t = Topologytranslator()

        # Read and load all JSON files
        all_nodes = []
        for file_name in DOMAIN_FILES:
            with open(file_name, "r") as file:
                data = json.load(file)
                all_nodes.append(data)

        # Pass the list to to_sdx_topology_json for testing
        result = d_t.to_sdx_topology_json(all_nodes)
        # print("Combined topology result:", result)
        self.assertIsNotNone(result)

    def test_sdx_topology_validate(self):
        d_t = Topologytranslator()

        # Read and load all JSON files
        all_nodes = []
        for file_name in DOMAIN_FILES:
            with open(file_name, "r") as file:
                data = json.load(file)
                all_nodes.append(data)

        # Get the combined topology JSON
        topology_json = d_t.to_sdx_topology_json(all_nodes)

        # Validate the topology
        is_valid = Topologytranslator.sdx_topology_validate(
            json.loads(topology_json)
        )
        print("Is the topology valid?", is_valid)
        self.assertTrue(is_valid)


if __name__ == "__main__":
    unittest.main()
