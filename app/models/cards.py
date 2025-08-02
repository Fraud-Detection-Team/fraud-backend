from pydantic import BaseModel


class CompromisedCard(BaseModel):
    id: str
    client_id: str
    status: str = "compromised"
