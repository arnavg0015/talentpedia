from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base
from datetime import datetime

class Competition(Base):
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String)          # STEM, Arts, Sports, etc.
    location_city = Column(String)
    location_country = Column(String)
    registration_deadline = Column(String)
    event_date = Column(String)
    url = Column(String)
    is_virtual = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)