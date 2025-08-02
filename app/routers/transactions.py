from fastapi import APIRouter, HTTPException
from ..data.loader import load_transactions, load_users, load_zip_coordinates
from ..utils.geo import haversine
from ..models.transactions import LocationRiskResponse

router = APIRouter()
transactions = load_transactions()
users = load_users().set_index("id")
zip_coords = load_zip_coordinates()

@router.get("/transactions/{transaction_id}/location-risk", response_model=LocationRiskResponse)
def check_location_risk(transaction_id: str, threshold_km: float = 100.0):
    tx = transactions[transactions["id"] == transaction_id]
    if tx.empty:
        raise HTTPException(status_code=404, detail="Transaction not found")

    tx = tx.iloc[0]
    client_id = str(tx["client_id"])
    merchant_zip = str(tx["zip"]).zfill(5)

    if client_id not in users.index:
        raise HTTPException(status_code=404, detail="User not found")
    if merchant_zip not in zip_coords:
        raise HTTPException(status_code=404, detail="Merchant ZIP not found")

    user = users.loc[client_id]
    user_lat, user_lon = user["latitude"], user["longitude"]
    merchant_lat, merchant_lon = zip_coords[merchant_zip]["latitude"], zip_coords[merchant_zip]["longitude"]

    distance = haversine(user_lat, user_lon, merchant_lat, merchant_lon)
    risk = "High" if distance > threshold_km else "Low"

    return LocationRiskResponse(distance_km=round(distance, 2), risk=risk)
