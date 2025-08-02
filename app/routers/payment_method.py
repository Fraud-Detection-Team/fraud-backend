from fastapi import APIRouter
from typing import List
from ..preload import transactions_df, fraud_labels
from ..models.payment_method import PaymentMethodFraudStat

router = APIRouter(prefix="/payment_method", tags=["Payment Method"])

@router.get("/fraud/by-payment-method", response_model=List[PaymentMethodFraudStat])
def fraud_by_payment_method():
    df = transactions_df.copy()

    # Add fraud label
    df["id"] = df["id"].astype(str).str.strip()
    clean_labels = {str(k).strip(): v.strip().lower() for k, v in fraud_labels.items()}
    df["fraud"] = df["id"].map(clean_labels).fillna("no")

    result = []
    for method in df["use_chip"].dropna().unique():
        subset = df[df["use_chip"] == method]
        total = len(subset)
        frauds = (subset["fraud"] == "yes").sum()
        fraud_rate = round(frauds / total, 4) if total else 0.0

        result.append(PaymentMethodFraudStat(
            method=method,
            total=total,
            frauds=frauds,
            fraud_rate=fraud_rate
        ))

    return result
