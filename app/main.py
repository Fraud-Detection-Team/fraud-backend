from fastapi import FastAPI
from pydantic import BaseModel
from routers import cards, merchants, users, transactions, fraud, payment_method, top5_mcc, top_users, state_fraud, monthly_transactions

app = FastAPI()

# Include Routers
app.include_router(cards.router)
app.include_router(merchants.router)
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(fraud.router)
app.include_router(payment_method.router)
app.include_router(top5_mcc.router)
app.include_router(top_users.router)
app.include_router(state_fraud.router)
app.include_router(monthly_transactions.router)