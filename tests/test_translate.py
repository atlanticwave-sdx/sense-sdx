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


import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from sense_sdx.translate import Requesttranslator


class RequestTranslatorTests(unittest.TestCase):
    def test_from_sdx_request_json(self):
        request_path = (
            Path(__file__).resolve().parent
            / "data"
            / "test-request-amlight_sax-p2p-v2.json"
        )
        request_json = request_path.read_text()

        mock_connection = SimpleNamespace(
            id="urn:sdx:connection:ampath.net:Ampath3:50-sax.net:Sax01:50",
            name="new-connection",
            endpoints=[
                SimpleNamespace(
                    port_uri="urn:sdx:port:ampath.net:Ampath3:50",
                    vlan_tag="302",
                ),
                SimpleNamespace(
                    port_uri="urn:sdx:port:sax.net:Sax01:50",
                    vlan_tag="302",
                ),
            ],
            qos_metrics=SimpleNamespace(min_bw=2),
        )

        with patch("sense_sdx.translate.ConnectionHandler") as mock_handler:
            mock_handler.return_value.import_connection_data.return_value = (
                mock_connection
            )

            translator = Requesttranslator()
            intent = translator.from_sdx_request_json(request_json)

        mock_handler.return_value.import_connection_data.assert_called_once_with(
            json.loads(request_json)
        )
        self.assertEqual(intent.service_instance_id, mock_connection.id)
        self.assertEqual(intent.data.connections[0].name, mock_connection.name)
        self.assertEqual(
            [t.uri for t in intent.data.connections[0].terminals],
            [endpoint.port_uri for endpoint in mock_connection.endpoints],
        )
        self.assertEqual(intent.data.connections[0].bandwidth.capacity, "2")


if __name__ == "__main__":
    unittest.main()
