from fastapi import APIRouter, Query, HTTPException
from preload import transactions_df, fraud_labels, mcc_dict
from ..models.merchants import MerchantRiskResponse

router = APIRouter(prefix="/merchants", tags=["Merchants"])

@router.get("/risk", response_model=MerchantRiskResponse)
def get_merchant_risk(mcc: str = Query(..., description="MCC code like 5812")):
    # Filter by MCC
    mcc_tx = transactions_df[transactions_df["mcc"].astype(str) == mcc]

    if mcc_tx.empty:
        raise HTTPException(status_code=404, detail="No transactions found for this MCC")

    # Count frauds using fraud_labels
    fraud_count = mcc_tx["id"].apply(lambda tx_id: fraud_labels.get(tx_id, "no") == "yes").sum()

    total_count = len(mcc_tx)
    rate = round(fraud_count / total_count, 4)

    return MerchantRiskResponse(
        mcc=mcc,
        category=mcc_dict.get(mcc, "Unknown"),
        total_transactions=total_count,
        fraud_transactions=fraud_count,
        fraud_rate=rate
    )
