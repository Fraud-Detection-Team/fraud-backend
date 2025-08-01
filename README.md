# 🛡️ Fraud Detection API – FastAPI Backend

This is a backend API service for detecting fraudulent transactions using a machine learning model. Built with **FastAPI**, the project supports various endpoints to assess fraud risks, user behavior, merchant category risk, and more.

## 🚀 Features

- Predict transaction fraud using a trained ML model
- Identify compromised cards (e.g., leaked on the dark web)
- Analyze fraud risk per merchant category
- Compare user spending against income
- Detect location-based transaction anomalies

---

## 📦 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/fraud/predict` | Predict whether a transaction is fraudulent |
| `GET`  | `/cards/compromised` | List cards flagged as compromised |
| `GET`  | `/merchants/risk?mcc=XXXX` | Return fraud risk score for a merchant category |
| `GET`  | `/users/{client_id}/spending` | Analyze user's spending vs. reported income |
| `GET`  | `/transactions/{transaction_id}/location-risk` | Detect geographic risk based on transaction distance |

---

## 🧠 ML Model

The fraud detection model is trained using a labeled dataset of transactions and fraud labels. The model is stored locally as a `.pkl` file and loaded at runtime via the `/fraud/predict` endpoint.

If the model file is not committed due to size (e.g. >100MB), either use Git LFS or retrain locally using:

```bash
python app/train_model.py
```

## 📁 Project Structure
```bash
fraud_detection_api/
├── app/
│   ├── data/              # Input datasets
│   ├── models/            # ML model + schemas
│   ├── routers/           # FastAPI route handlers
│   ├── utils/             # Utility functions (geo calculations, etc.)
│   ├── main.py            # Entry point for the FastAPI app
│   ├── train_model.py     # Model training script
│   └── preload.py         # Data preprocessing/loading
├── requirements.txt
└── README.md
```
## ⚙️ Setup Instructions
1. Clone the repository
```bash
git clone https://github.com/Fraud-Detection-Team/fraud-backend.git
cd fraud-backend
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the API
```bash
uvicorn app.main:app --reload
```

5. Access docs

   Go to http://localhost:8000/docs to view Swagger UI.


