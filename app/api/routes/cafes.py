from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.cafe import Cafe
from app.schemas.cafe import CafeDetailResponse, CafeSearchResponse

from app.services.cafe_service import search_and_save_cafes, cafe_to_response, get_or_create_summary

router = APIRouter(prefix="/cafes", tags=["cafes"])

MIN_CAFE_RESULT_COUNT = 3

@router.get("/search", response_model=CafeSearchResponse)
async def search_cafes (
    query: str = Query("카페"),
    x: float | None = None,
    y: float | None = None,
    radius: int = 1000,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    cafes = search_and_save_cafes(
        db=db,
        query=query,
        x=x,
        y=y,
        radius=radius,
        limit=limit
    )

    low_result_count = len(cafes) < MIN_CAFE_RESULT_COUNT

    return CafeSearchResponse(
        count=len(cafes),
        low_result_count=low_result_count,
        message = (
            "근처 카페가 적어요. 반경을 넓히면 더 많은 후보를 볼 수 있어요."
            if low_result_count
            else None
        ),
        cafes=cafes,
    )


@router.get("/{place_id}", response_model=CafeDetailResponse)
async def get_cafe_detail(
    place_id: str,
    db: Session = Depends(get_db),
):
    cafe = db.query(Cafe).filter(Cafe.place_id == place_id).first()

    if cafe is None:
        raise HTTPException(status_code=404, detail="Cafe Not Found")

    cafe.ai_summary = await get_or_create_summary(cafe, db)

    return cafe


