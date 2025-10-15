from pydantic import BaseModel


class Bandwidth(BaseModel):
    qos_class: str
    capacity: str


class Terminal(BaseModel):
    vlan_tag: str
    uri: str


class Connection(BaseModel):
    name: str
    bandwidth: Bandwidth
    terminals: list[Terminal]


class Data(BaseModel):
    type: str
    connections: list[Connection]


class Intent(BaseModel):
    service_instance_uuid: str
    data: Data  # Use the new Data class for the 'data' attribute
    service: str
    options: list
    service_profile_uuid: str
    queries: list
