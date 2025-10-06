from pydantic import BaseModel


class instance(BaseModel):
    intents: list
    alias: str
    referenceUUID: str
    profileUUID: str
    state: str
    owner: str
    lastState: str
    timestamp: str
    archived: bool
