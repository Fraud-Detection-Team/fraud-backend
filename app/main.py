from fastapi import FastAPI
from pydantic import BaseModel
from routers import cards, merchants, users, transactions, fraud

app = FastAPI()

# Include Routers
app.include_router(cards.router)
app.include_router(merchants.router)
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(fraud.router)
