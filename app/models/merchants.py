from pydantic import BaseModel


class MerchantRiskResponse(BaseModel):
    mcc: str
    category: str
    total_transactions: int
    fraud_transactions: int
    fraud_rate: float
