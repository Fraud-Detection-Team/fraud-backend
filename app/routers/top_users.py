from fastapi import APIRouter
from typing import List
from ..models.users import SpendingAnalysis
from ..preload import transactions_df, users_df

router = APIRouter(prefix="/TopUsers", tags=["Top Users Spending"])

@router.get("/spending/top-users", response_model=List[SpendingAnalysis])
def top_spending_users(limit: int = 5, sort_by: str = "ratio"):
    # Merge transactions with users
    spending = transactions_df.groupby("client_id")["amount"].sum().reset_index()
    merged = spending.merge(users_df[["id", "yearly_income"]], left_on="client_id", right_on="id")

    # Compute stats
    merged["monthly_spending"] = merged["amount"] / 12
    merged["spending_ratio"] = merged["amount"] / merged["yearly_income"]

    # Rename for output clarity
    merged.rename(columns={"amount": "total_spending"}, inplace=True)

    # Sort
    if sort_by == "spending":
        merged = merged.sort_values("total_spending", ascending=False)
    else:
        merged = merged.sort_values("spending_ratio", ascending=False)

    # Limit
    top_users = merged.head(limit)

    # Format result
    return [
        SpendingAnalysis(
            user_id=str(row["client_id"]),
            income=row["yearly_income"],
            total_spending=row["total_spending"],
            monthly_spending=round(row["monthly_spending"], 2),
            spending_ratio=round(row["spending_ratio"], 2),
        )
        for _, row in top_users.iterrows()
    ]
