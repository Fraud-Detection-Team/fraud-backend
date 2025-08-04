from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .routers import (
    cards, merchants, users, transactions,
    fraud, payment_method, top5_mcc,
    top_users, state_fraud, monthly_transactions
)

# Auth modules
from .auth import auth, schemas, deps
from .database.db import get_db  # make sure this exists

app = FastAPI()

# Auth: Login endpoint
@app.post("/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)  # form_data.username = email
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# Example: protect any endpoint
@app.get("/secure/test")
def secure_route(current_user: schemas.User = Depends(deps.get_current_user)):
    return {"message": f"Welcome, {current_user.email}!"}

# Routers
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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
