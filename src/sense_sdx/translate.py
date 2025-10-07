import sdx_datamodel

from sdx_datamodel.models.topology import *

class Topologytranslator:
    def __init__(self, topology: Topology):
        self.topology = topology

    def sense_parse(self) -> Topology:
        # Assuming the input is a dictionary representing the topology
        nodes = [Node(**node) for node in self.topology.get('nodes', [])]
        links = [Link(**link) for link in self.topology.get('links', [])]
        return Topology(nodes=nodes, links=links)

    def to_sdx(self) -> sdx_datamodel.models.topology.Topology:
        sdx_topology = sdx_datamodel.models.topology.Topology()

        # Translate nodes
        for node in self.topology.nodes:
            sdx_node = sdx_datamodel.models.topology.Node(
                id=node.id,
                name=node.name,
                type=node.type,
                location=node.location
            )
            sdx_topology.nodes.append(sdx_node)

        # Translate links
        for link in self.topology.links:
            sdx_link = sdx_datamodel.models.topology.Link(
                id=link.id,
                source=link.source,
                destination=link.destination,
                capacity=link.capacity,
                latency=link.latency
            )
            sdx_topology.links.append(sdx_link)

        return sdx_topology