from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from .database import Base
from datetime import datetime

class Competition(Base):
    __tablename__ = "competitions"

    id             = Column(Integer, primary_key=True, index=True)
    title          = Column(String(255), nullable=False)
    category       = Column(String(50))       # STEM, Arts, Sports, Other
    description    = Column(Text)
    location_city  = Column(String(100))
    location_state = Column(String(100))
    location_country = Column(String(100), default="US")
    is_virtual     = Column(Boolean, default=False)
    registration_deadline = Column(String(50))
    event_date     = Column(String(50))
    age_min        = Column(Integer)
    age_max        = Column(Integer)
    url            = Column(String(500))
    source         = Column(String(100))      # eventbrite, first_robotics, manual
    created_at     = Column(DateTime, default=datetime.utcnow)