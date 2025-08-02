from pydantic import BaseModel


class FraudInput(BaseModel):
    amount: float
    use_chip: str
    mcc: int
    errors: str
