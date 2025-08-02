from fastapi import APIRouter
from typing import List
from preload import transactions_df, fraud_labels, mcc_dict
from models.merchants import MerchantRiskResponse

router = APIRouter(prefix="/Top5Merchant", tags=["Top 5 Merchant MCC"])

@router.get("/fraud/by-mcc", response_model=List[MerchantRiskResponse])
def fraud_by_mcc():
    df = transactions_df.copy()
    df["fraud"] = df["id"].map(fraud_labels).fillna("No")
    df["mcc"] = df["mcc"].astype(str)

    stats = []
    for mcc_code in df["mcc"].dropna().unique():
        subset = df[df["mcc"] == mcc_code]
        total = len(subset)
        frauds = (subset["fraud"] == "Yes").sum()
        rate = round(frauds / total, 4) if total else 0.0
        category = mcc_dict.get(mcc_code, "Unknown")

        stats.append(MerchantRiskResponse(
            mcc=mcc_code,
            category=category,
            total_transactions=total,
            fraud_transactions=frauds,
            fraud_rate=rate
        ))

    return sorted(stats, key=lambda x: x.fraud_rate, reverse=True)
