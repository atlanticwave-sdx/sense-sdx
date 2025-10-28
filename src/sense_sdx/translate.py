import json

import sdx_datamodel
from sdx_datamodel.models.link import Link
from sdx_datamodel.models.node import *
from sdx_datamodel.models.topology import *
from sdx_datamodel.parsing.connectionhandler import ConnectionHandler
from sdx_datamodel.parsing.topologyhandler import TopologyHandler
from sdx_datamodel.validation.topologyvalidator import TopologyValidator

from sense_sdx.models.domain import Domain, Peer_point
from sense_sdx.models.intent import (
    Bandwidth,
    Connection,
    Data,
    Intent,
    Terminal,
)

TOPOLOGY_DEFAULT_NAME = "sense"
TOPOLOGY_DEFAULT_URI = "urn:sdx:topology:sense.net"


class Topologytranslator:
    def __init__(self):
        self.node_json = None

    def to_sdx_node_json(self, domain: json) -> json:
        domain = Domain.model_validate(domain)

        # Convert the domain instance to a JSON object with the required property mapping
        node_json = {
            "id": domain.domain_uri,
            "name": domain.domain_name or domain.domain_uri.split(":")[3],
            "location": {
                "address": domain.domain_name
                or domain.domain_uri.split(":")[3],
                "iso3166_2_lvl4": "BR-CE",
                "latitude": 25.77,
                "longitude": -80.19,
            },
            "ports": [
                {
                    "id": peer_point.port_uri,
                    "name": peer_point.port_name,
                    "nni": peer_point.peer_uri,
                    "services": {
                        "l2vpn-ptp": {
                            "vlan_range": peer_point.port_vlan_pool.split(",")
                        }
                    },
                }
                for peer_point in domain.peer_points
            ],
        }

        return json.dumps(node_json)

    def to_sdx_links_json(self, nodes: list) -> json:
        links = []
        seen = set()
        node_ports = {
            port["id"].replace(" ", ""): (node["id"], port)
            for node in nodes
            for port in node.get("ports", [])
        }
        print("Node ports mapping:", node_ports.keys())
        for node in nodes:
            for port in node.get("ports", []):
                nni = (
                    port.get("nni").replace(" ", "")
                    if port.get("nni")
                    else None
                )
                if nni and nni in node_ports:
                    peer_node_id, peer_port = node_ports[nni]
                    # Check if the peer port's nni points back to this port
                    if peer_port.get("nni").replace(" ", "") == port[
                        "id"
                    ].replace(" ", ""):
                        # Create a unique link id by sorting the two port ids
                        link_ports = tuple(
                            sorted([port["id"], peer_port["id"]])
                        )
                        if link_ports not in seen:
                            seen.add(link_ports)
                            link_obj = Link(
                                id=f"{link_ports[0]}-{link_ports[1]}",
                                name=f"{link_ports[0]}-{link_ports[1]}",
                                ports=[port["id"], peer_port["id"]],
                            )
                            links.append(link_obj.to_dict())
        print("Total links created:", len(links))
        return json.dumps(links)

    def to_sdx_topology_json(self, domains: list) -> json:
        domains = [
            domain
            for domain in domains
            if domain.get("peer_points", None) is not None
        ]
        topology_json = {
            "id": TOPOLOGY_DEFAULT_URI,
            "name": TOPOLOGY_DEFAULT_NAME,
            "nodes": [
                json.loads(self.to_sdx_node_json(domain)) for domain in domains
            ],
        }

        topology_json["links"] = json.loads(
            self.to_sdx_links_json(topology_json["nodes"])
        )

        return json.dumps(topology_json)

    def sdx_topology_validate(topology_json: json) -> bool:
        topology = TopologyHandler().import_topology_data(topology_json)
        validator = TopologyValidator(topology)
        is_valid = validator.is_valid()
        return is_valid


class Requesttranslator:
    def from_sdx_request_json(self, connection_json: json) -> json:
        connection = ConnectionHandler().import_connection_data(
            json.loads(connection_json)
        )

        terminals = [
            Terminal(
                vlan_tag=endpoint.vlan_tag,
                uri=endpoint.port_uri,
            )
            for endpoint in connection.endpoints
        ]

        bandwidth = Bandwidth(
            qos_class="guaranteed",
            capacity=str(connection.qos_metrics.min_bw),
        )
        intent = Intent(
            type="connection_request",
            service_instance_id=connection.id,
            service="dnc",
            service_profile_uuid="default-service-profile-uuid",
            data=Data(
                type="Multi-Path P2P VLAN",
                connections=[
                    Connection(
                        name=connection.name,
                        bandwidth=bandwidth,
                        terminals=terminals,
                    )
                ],
            ),
        )
        return intent.model_dump_json(indent=2)


class Responsetranslator:
    def to_sdx_response_json(self, intent: Intent) -> json:
        connection = intent.data.connections[0]
        endpoints = [
            sdx_datamodel.models.endpoint.Endpoint(
                port_uri=terminal.uri,
                vlan_tag=terminal.vlan_tag,
            )
            for terminal in connection.terminals
        ]
        sdx_connection = sdx_datamodel.models.connection.Connection(
            id=intent.service_instance_id,
            name=connection.name,
            qos_metrics=sdx_datamodel.models.qos.QoSMetrics(
                min_bw=int(connection.bandwidth.capacity)
            ),
            endpoints=endpoints,
        )
        return json.dumps(sdx_connection.to_dict())
