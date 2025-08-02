from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_compromised_cards_endpoint():
    response = client.get("/cards/compromised")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Check if response is a list
    assert all("id" in card and "client_id" in card for card in response.json())  # Check structure

def test_fraud_prediction():
    sample_input = {
        "amount": 120.5,
        "use_chip": "Swipe Transaction",
        "mcc": "5999",
        "errors": "None"
    }
    
    response = client.post("/fraud/predict", json=sample_input)
    
    assert response.status_code == 200
    assert "fraud_prediction" in response.json()
    assert response.json()["fraud_prediction"] in ["Yes", "No"]

def test_get_merchant_risk_exists():
    response = client.get("/merchants/risk", params={"mcc": "5812"})
    assert response.status_code == 200
    
    data = response.json()
    assert "mcc" in data
    assert "category" in data
    assert "total_transactions" in data
    assert "fraud_transactions" in data
    assert "fraud_rate" in data

def test_get_merchant_risk_not_found():
    response = client.get("/merchants/risk", params={"mcc": "9999"})
    assert response.status_code == 404
    assert response.json()["detail"] == "No transactions found for this MCC"

def test_monthly_transactions_endpoint():
    response = client.get("/monthly_transactions/transactions/by-month")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_fraud_by_payment_method():
    response = client.get("/payment_method/fraud/by-payment-method")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)  # Check the response is a list
    
    for item in data:
        assert "method" in item
        assert "total" in item
        assert "frauds" in item
        assert "fraud_rate" in item

def test_fraud_by_payment_method_response_content():
    response = client.get("/payment_method/fraud/by-payment-method")
    assert response.status_code == 200
    
    data = response.json()

    # Example check: ensure a known payment method exists
    methods = [item["method"] for item in data]
    assert any(method in ["Swipe Transaction", "Online", "Chip"] for method in methods)

def test_transaction_volume_by_state():
    response = client.get("/state_fraud/volume/by-state")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)  # Check the response is a list
    
    for item in data:
        assert "state" in item
        assert "transactions" in item
        assert "frauds" in item
        assert "fraud_rate" in item

def test_transaction_volume_by_state_content():
    response = client.get("/state_fraud/volume/by-state")
    assert response.status_code == 200
    
    data = response.json()

    # Example check: ensure a known state exists
    states = [item["state"] for item in data]
    assert "CA" in states 

def test_top_users_endpoint():
    response = client.get("/TopUsers/spending/top-users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_top5_mcc_endpoint():
    response = client.get("/Top5Merchant/fraud/by-mcc")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_transactions_endpoint():
    response = client.get("/transactions/{transaction_id}/location-risk", params={"threshold_km": 100.0})
    assert response.status_code == 404
    assert response.json()["detail"] == "Transaction not found"

def test_users_endpoint():
    response = client.get("/users/{client_id}/spending")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"



