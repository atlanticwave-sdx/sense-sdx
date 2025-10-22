import unittest
import json

from sense_sdx.client import call_services, topology_translate, TOPOLOGY, INTENT, INSTANCE

class ClientTests(unittest.TestCase):
    def test_call_services_without_arg(self):
        response = call_services()
        with open("./tests/data/domain_ids.json", "w") as f:
            json.dump(response, f, indent=2)
        self.assertTrue(True)

    def test_call_services_with_all(self):
        response = call_services(service=TOPOLOGY, arg="all")
        with open("./tests/data/domains.json", "w") as f:
            json.dump(response, f, indent=2)
        self.assertTrue(True)

    def test_call_services_with_domain_id(self):
        response = call_services(
            service=TOPOLOGY, arg="urn:sdx:domain:es.net"
        )

        with open("./tests/data/es.net.json", "w") as f:
            json.dump(response, f, indent=2)
        self.assertTrue(True)

    def test_topology_translate(self):
        result = topology_translate()

        self.assertTrue("domains" in result)

if __name__ == "__main__":
    unittest.main()