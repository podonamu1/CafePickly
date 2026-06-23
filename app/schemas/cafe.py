from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CafeBase(BaseModel):
    place_id: str
    place_name: str
    category_name: str | None = None
    address_name: str | None = None
    road_address_name: str | None = None
    phone: str | None = None
    place_url: str | None = None

    x: float | None = None
    y: float | None = None
    distance: int | None = None

    is_franchise: bool = False
    ai_summary: str | None = None
    summary_updated_at: datetime | None = None

    created_at: datetime
    updated_at: datetime

    score: float | None =  None

class CafeListItem(CafeBase):
    model_config = ConfigDict(from_attributes=True)

class CafeDetailResponse(CafeBase):
    model_config = ConfigDict(from_attributes=True)

class CafeSearchResponse(BaseModel):
    count: int
    low_result_count: bool
    message: str | None = None
    cafes: list[CafeListItem]
    suggested_radius: int | None = None