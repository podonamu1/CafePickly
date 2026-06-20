from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.sql import func

from app.db.base import Base

class Cafe(Base):
    __tablename__ = "cafes"

    id = Column(Integer, primary_key=True, index=True)

    place_id = Column(String, unique=True, index=True, nullable=False)
    place_name = Column(String, nullable=False)

    category_name = Column(String, nullable=True)
    address_name = Column(String, nullable=True)
    road_address_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    place_url = Column(String, nullable=True)

    x = Column(String, nullable=True)
    y = Column(String, nullable=True)
    distance = Column(String, nullable=True)

    is_franchsise = Column(Boolean, default=False, nullable=False)
    ai_summary = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )