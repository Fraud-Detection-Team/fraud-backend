from fastapi import APIRouter, HTTPException
from preload import transactions_df, users_df
from ..models.users import SpendingAnalysis

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{client_id}/spending", response_model=SpendingAnalysis)
def analyze_user_spending(client_id: str):
    # Filter user
    user_data = users_df[users_df["id"] == client_id]
    if user_data.empty:
        raise HTTPException(status_code=404, detail="User not found")

    income = float(user_data.iloc[0]["yearly_income"])

    # Filter transactions
    user_tx = transactions_df[transactions_df["client_id"] == client_id]

    if user_tx.empty:
        return SpendingAnalysis(
            user_id=client_id,
            income=income,
            total_spending=0.0,
            monthly_spending=0.0,
            spending_ratio=0.0
        )

    # Calculate monthly spending and ratio
    total = user_tx["amount"].sum()
    monthly = round(total / 12, 2)
    ratio = round(total / income, 2)

    return SpendingAnalysis(
        user_id=client_id,
        income=income,
        total_spending=total,
        monthly_spending=monthly,
        spending_ratio=ratio
    )
