import joblib
from fastapi import APIRouter, Depends
from ..models.fraud import FraudInput
from pathlib import Path
from ..auth.deps import get_current_user
from ..auth.schemas import User


router = APIRouter()


model_path = Path(__file__).resolve().parent.parent / "models" / "fraud_model_v2.pkl"
model = joblib.load(model_path)


@router.post("/fraud/predict")
async def predict_fraud(
    transaction: FraudInput,
    current_user: User = Depends(get_current_user)
):
    mcc_code = int(transaction.mcc)
    error_code = str(transaction.errors)

    mcc_encoded = mcc_code  
    error_encoded = 0

    features = [[
        transaction.amount,
        1 if transaction.use_chip.lower() == "swipe transaction" else 0,
        mcc_encoded,
        error_encoded,
    ]]

    prediction = model.predict(features)[0]

    return {
        "fraud_prediction": "Yes" if prediction == 1 else "No",
        "predicted_by": current_user.username  # Optional: return user info for traceability
    }

