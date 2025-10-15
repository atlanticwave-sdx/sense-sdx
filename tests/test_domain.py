import unittest
from sense_sdx.models.domain import Domain, Peer_point
import json


class TestDomainModel(unittest.TestCase):
    def setUp(self):
        # Load example JSON file
        with open("./tests/data/mren8700.json", "r") as file:
            self.example_data = json.load(file)

    def test_peer_point_creation(self):
        peer_data = self.example_data["peer_points"][0]
        peer = Peer_point(
            port_name=peer_data["port_name"],
            port_uri=peer_data["port_uri"],
            peer_capacity=peer_data["peer_capacity"],
            peer_vlan_pool=peer_data["peer_vlan_pool"],
            port_vlan_pool=peer_data["port_vlan_pool"],
            port_capacity=peer_data["port_capacity"],
            peer_uri=peer_data["peer_uri"],
        )
        self.assertEqual(peer.port_name, peer_data["port_name"])
        self.assertEqual(peer.port_uri, peer_data["port_uri"])
        self.assertEqual(peer.peer_capacity, peer_data["peer_capacity"])
        self.assertEqual(peer.peer_vlan_pool, peer_data["peer_vlan_pool"])
        self.assertEqual(peer.port_vlan_pool, peer_data["port_vlan_pool"])
        self.assertEqual(peer.port_capacity, peer_data["port_capacity"])
        self.assertEqual(peer.peer_uri, peer_data["peer_uri"])

    def test_domain_creation(self):
        domain_data = self.example_data
        domain_instance = Domain(
            domain_uri=domain_data["domain_uri"],
            domain_name=domain_data["domain_name"],
            peer_points=[
                Peer_point(
                    port_name=peer["port_name"],
                    port_uri=peer["port_uri"],
                    peer_capacity=peer["peer_capacity"],
                    peer_vlan_pool=peer["peer_vlan_pool"],
                    port_vlan_pool=peer["port_vlan_pool"],
                    port_capacity=peer["port_capacity"],
                    peer_uri=peer["peer_uri"],
                )
                for peer in domain_data["peer_points"]
            ],
        )

        print(domain_instance)

        self.assertEqual(domain_instance.domain_uri, domain_data["domain_uri"])
        self.assertEqual(
            domain_instance.domain_name, domain_data["domain_name"]
        )
        self.assertEqual(
            len(domain_instance.peer_points), len(domain_data["peer_points"])
        )

        for i, peer in enumerate(domain_instance.peer_points):
            peer_data = domain_data["peer_points"][i]
            self.assertEqual(peer.port_name, peer_data["port_name"])
            self.assertEqual(peer.port_uri, peer_data["port_uri"])
            self.assertEqual(peer.peer_capacity, peer_data["peer_capacity"])
            self.assertEqual(peer.peer_vlan_pool, peer_data["peer_vlan_pool"])
            self.assertEqual(peer.port_vlan_pool, peer_data["port_vlan_pool"])
            self.assertEqual(peer.port_capacity, peer_data["port_capacity"])
            self.assertEqual(peer.peer_uri, peer_data["peer_uri"])

    def test_domain(self):
        try:
            mren8700 = Domain.model_validate(self.example_data)
            self.assertTrue(True)  # Assert True if no exception is raised
        except Exception as e:
            self.fail(f"Domain.model_validate raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
