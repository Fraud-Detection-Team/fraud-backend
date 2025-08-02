from pydantic import BaseModel

class PaymentMethodFraudStat(BaseModel):
    method: str
    total: int
    frauds: int
    fraud_rate: float
