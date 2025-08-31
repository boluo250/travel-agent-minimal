from fastapi import APIRouter, HTTPException
from app.schemas.plan import PlanRequest, KmTravelResponse
from app.services.gaode_mcp import AmapClient
from app.utils.itinerary import build_itinerary, to_km_travel

router = APIRouter()


@router.post("/plan_km", response_model=KmTravelResponse)
def create_plan_km(req: PlanRequest):
    client = AmapClient()
    try:
        raw = build_itinerary(
            client=client,
            city=req.city,
            days=req.days,
            interests=req.interests,
            starting_point=req.starting_point,
            start_date=req.start_date,
        )
        shaped = to_km_travel(raw)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Upstream error: {e}")
    return shaped

