from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from .database import get_db
from .models import Competition

app = FastAPI(title="Talentpedia API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Talentpedia API", "status": "running"}

@app.get("/competitions")
def get_competitions(
    db: Session = Depends(get_db),
    category: Optional[str] = Query(None, description="STEM, Arts, Sports, Other"),
    state: Optional[str] = Query(None, description="e.g. NC, NY"),
    is_virtual: Optional[bool] = Query(None),
    limit: int = Query(20, le=100),
):
    query = db.query(Competition)
    
    if category:
        query = query.filter(Competition.category == category)
    if state:
        query = query.filter(Competition.location_state == state)
    if is_virtual is not None:
        query = query.filter(Competition.is_virtual == is_virtual)
    
    competitions = query.order_by(Competition.event_date).limit(limit).all()
    
    return [
        {
            "id": c.id,
            "title": c.title,
            "category": c.category,
            "city": c.location_city,
            "state": c.location_state,
            "event_date": c.event_date,
            "registration_deadline": c.registration_deadline,
            "url": c.url,
            "is_virtual": c.is_virtual,
            "age_min": c.age_min,
            "age_max": c.age_max,
        }
        for c in competitions
    ]

@app.get("/competitions/{id}")
def get_competition(id: int, db: Session = Depends(get_db)):
    comp = db.query(Competition).filter(Competition.id == id).first()
    if not comp:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Competition not found")
    return comp