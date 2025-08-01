from pydantic import BaseModel

class LocationRiskResponse(BaseModel):
    distance_km: float
    risk: str  # "High" or "Low"
