from pydantic import BaseModel


class SpendingAnalysis(BaseModel):
    user_id: str
    income: float
    total_spending: float
    monthly_spending: float
    spending_ratio: float
