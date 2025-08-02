from fastapi import APIRouter
from ..models.cards import CompromisedCard
from ..preload import cards_df

router = APIRouter(prefix="/cards", tags=["Cards"])

@router.get("/compromised", response_model=list[CompromisedCard])
def get_compromised_cards():
    compromised = cards_df[cards_df["is_compromised"] == True]

    results = [
        CompromisedCard(
            id=row["id"],
            client_id=row["client_id"] if "client_id" in row else "unknown"
        )
        for _, row in compromised.iterrows()
    ]
    return results
