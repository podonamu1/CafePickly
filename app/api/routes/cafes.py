from fastapi import APIRouter
from app.services.cafe_service import get_recommend_cafes

router = APIRouter(prefix="/cafes", tags=["cafes"])

@router.get("/")
def recommend_cafes(
        lat: float, lon: float, radius: int = 1000, limit: int = 5
):
    return get_recommend_cafes(lat, lon, radius, limit)

