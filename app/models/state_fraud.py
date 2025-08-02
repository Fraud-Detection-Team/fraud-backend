from pydantic import BaseModel

class StateFraudVolume(BaseModel):
    state: str
    transactions: int
    frauds: int
    fraud_rate: float
