from pydantic import BaseModel

class MonthlyTransactionStat(BaseModel):
    month: str
    transactions: int
    frauds: int
    fraud_rate: float