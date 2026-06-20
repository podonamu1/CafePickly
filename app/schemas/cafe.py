from pydantic import BaseModel, ConfigDict

class CafeBase(BaseModel):
    place_id: str
    place_name: str
    category_name: str | None = None
    address_name: str | None = None
    road_address_name: str | None = None
    phone: str | None = None
    place_url: str | None = None
    x: str | None = None
    y: str | None = None
    distance: str | None = None
    is_franchise: bool = False
    ai_summary: str | None = None

class CafeListItem(CafeBase):
    model_config = ConfigDict(from_attributes=True)

class CafeDetailResponse(CafeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)