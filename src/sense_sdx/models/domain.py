from pydantic import BaseModel


class Peer_point(BaseModel):
    port_name: str
    port_uri: str
    peer_capacity: str
    peer_vlan_pool: str
    port_vlan_pool: str
    port_capacity: str
    peer_uri: str


class Domain(BaseModel):
    domain_uri: str
    domain_name: str
    peer_points: list[Peer_point]
