from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Talentpedia API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Talentpedia API is running"}

@app.get("/competitions")
def get_competitions():
    return [
        {"id": 1, "title": "Science Olympiad 2025", "category": "STEM", "location": "Durham, NC"},
        {"id": 2, "title": "National Art Awards", "category": "Arts", "location": "New York, NY"},
    ]