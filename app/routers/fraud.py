import joblib
from fastapi import APIRouter
from ..models.fraud import FraudInput

router = APIRouter()

base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "models", "fraud_model_v2.pkl")
model = joblib.load(model_path)

@router.post("/fraud/predict")
async def predict_fraud(transaction: FraudInput):
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
    return {"fraud_prediction": "Yes" if prediction == 1 else "No"}
