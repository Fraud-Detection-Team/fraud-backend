from fastapi import APIRouter
from typing import List
from preload import transactions_df, fraud_labels
from models.monthly_transactions import MonthlyTransactionStat
from fastapi import HTTPException
import pandas as pd

router = APIRouter(prefix="/monthly_transactions", tags=["Monthly Transactions"])

@router.get("/transactions/by-month", response_model=List[MonthlyTransactionStat])
def transactions_by_month():
    df = transactions_df.copy()

    # Ensure 'date' column exists and is parsed
    if "date" not in df.columns:
        raise HTTPException(status_code=400, detail="Date column not found in transactions")

    # Convert string date to datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])  # drop invalid dates
    df["month"] = df["date"].dt.to_period("M").astype(str)

    # Add fraud label
    df["fraud"] = df["id"].map(fraud_labels).fillna("No")

    # Group by month
    grouped = df.groupby("month").agg(
        transactions=("id", "count"),
        frauds=("fraud", lambda x: (x == "Yes").sum())
    ).reset_index()
    grouped["fraud_rate"] = (grouped["frauds"] / grouped["transactions"]).round(4)

    # Format for API response
    return [
        MonthlyTransactionStat(
            month=row["month"],
            transactions=row["transactions"],
            frauds=row["frauds"],
            fraud_rate=row["fraud_rate"]
        )
        for _, row in grouped.iterrows()
    ]