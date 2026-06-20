from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.cafe import Cafe
from app.schemas.cafe import CafeDetailResponse, CafeListItem

from app.services.cafe_service import search_and_save_cafes

router = APIRouter(prefix="/cafes", tags=["cafes"])

@router.get("/search", response_model=list[CafeListItem])
def search_cafes (
    query: str = Query("카페"),
    x: float | None = None,
    y: float | None = None,
    radius: int = 1000,
    db: Session = Depends(get_db)
):
    return search_and_save_cafes(
        db = db,
        query = query,
        x = x,
        y = y,
        radius = radius
    )

@router.get("/{place_id}", response_model=CafeDetailResponse)
def get_cafe_detail(
    place_id: str,
    db: Session = Depends(get_db),
):
    cafe = db.query(Cafe).filter(Cafe.place_id == place_id).first()

    if cafe is None:
        raise HTTPException(status_code=404, detail="Cafe Not Found")

    return cafe


