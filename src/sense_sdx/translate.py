import sdx_datamodel

from sdx_datamodel.models.topology import *
from sdx_datamodel.models.node import *

from sense_sdx.models.domain import Domain, Peer_point
import json


class Domaintranslator:
    def __init__(self):
        self.node_json = None

    def domain_to_sdx_node_json(self, domain: json) -> json:
        domain = Domain.model_validate(domain)

        # Convert the domain instance to a JSON object with the required property mapping
        node_json = {
            "id": domain.domain_name,
            "name": domain.domain_name,
            "ports": [
                {
                    "id": peer_point.port_uri,
                    "name": peer_point.port_name,
                    "nni": peer_point.peer_uri,
                    "services": {
                        "l2vpn-ptp": {"vlan_range": peer_point.port_vlan_pool}
                    },
                }
                for peer_point in domain.peer_points
            ],
        }

        return node_json

    def to_sdx_topology_json(self, domains: list) -> json:
        topology_json = {
            "id": "urn:sdx:topology:sense.net",
            "name": "sense",
            "nodes": [
                {self.domain_to_sdx_node_json(domain)} for domain in domains
            ],
        }

        return topology_json
