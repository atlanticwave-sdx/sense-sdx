from pydantic import BaseModel


class domain(BaseModel):
    domain_uri: str
    domain_name: str
    peer_points: list
    