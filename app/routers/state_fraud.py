from fastapi import APIRouter
from typing import List
from ..preload import transactions_df, fraud_labels
from ..models.state_fraud import StateFraudVolume

router = APIRouter(prefix="/state_fraud", tags=["State Fraud"])

@router.get("/volume/by-state", response_model=List[StateFraudVolume])
def transaction_volume_by_state():
    df = transactions_df.copy()
    df["fraud"] = df["id"].map(fraud_labels).fillna("No")
    df["merchant_state"] = df["merchant_state"].fillna("Unknown")

    result = []
    for state in df["merchant_state"].unique():
        subset = df[df["merchant_state"] == state]
        total = len(subset)
        frauds = (subset["fraud"] == "Yes").sum()
        fraud_rate = round(frauds / total, 4) if total else 0.0

        result.append(StateFraudVolume(
            state=state,
            transactions=total,
            frauds=frauds,
            fraud_rate=fraud_rate
        ))

    return sorted(result, key=lambda x: x.fraud_rate, reverse=True)
