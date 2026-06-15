import httpx, os, sys, base64
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine
from app.models import Competition
from app.database import Base

Base.metadata.create_all(bind=engine)

# ─── Devpost (Hackathons) ─────────────────────────────────────────────────────

def fetch_devpost():
    """Devpost has a stable unofficial API for student hackathons"""
    try:
        resp = httpx.get(
            "https://devpost.com/api/hackathons",
            params={
                "status[]": "upcoming",
                "order_by": "deadline",
                "per_page": 50
            },
            headers={"Accept": "application/json"},
            timeout=15
        )
        resp.raise_for_status()
        hackathons = resp.json().get("hackathons", [])
        print(f"✅  Devpost: {len(hackathons)} hackathons fetched")

        results = []
        for h in hackathons:
            results.append({
                "title": h.get("title", "")[:255],
                "category": "STEM",
                "description": h.get("tagline", "")[:500],
                "city": h.get("location", ""),
                "state": "",
                "country": "US",
                "event_date": (h.get("submission_period_dates", "") or "")[:10],
                "url": h.get("url", ""),
                "age_min": 13,
                "age_max": 25,
                "is_virtual": h.get("online_only", False),
                "source": "devpost"
            })
        return results

    except Exception as ex:
        print(f"❌  Devpost failed: {ex}")
        return []

# ─── FIRST Robotics ───────────────────────────────────────────────────────────

def fetch_first_robotics():
    username = os.getenv("FIRST_API_USERNAME")
    token    = os.getenv("FIRST_API_TOKEN")

    if not username or not token:
        print("⚠️  No FIRST credentials — skipping")
        return []

    credentials = base64.b64encode(f"{username}:{token}".encode()).decode()

    try:
        resp = httpx.get(
            "https://frc-events.firstinspires.org/v2.0/2025/events",
            headers={
                "Authorization": f"Basic {credentials}",
                "Accept": "application/json"
            },
            timeout=15
        )
        resp.raise_for_status()
        events = resp.json().get("Events", [])
        print(f"✅  FIRST Robotics: {len(events)} events fetched")

        return [{
            "title": f"FRC — {e.get('name', '')}",
            "category": "STEM",
            "description": e.get("typeName", ""),
            "city": e.get("city", ""),
            "state": e.get("stateprov", ""),
            "country": e.get("country", "US"),
            "event_date": (e.get("dateStart") or "")[:10],
            "url": "https://www.firstinspires.org/robotics/frc",
            "age_min": 14,
            "age_max": 18,
            "is_virtual": False,
            "source": "first_robotics"
        } for e in events]

    except Exception as ex:
        print(f"❌  FIRST Robotics failed: {ex} — check email confirmation")
        return []

# ─── Challenge.gov (US Government prize competitions) ─────────────────────────

def fetch_challengegov():
    """Fully open government API, no key needed"""
    try:
        resp = httpx.get(
            "https://www.challenge.gov/api/challenges/",
            params={"status": "open", "per_page": 50},
            timeout=15
        )
        resp.raise_for_status()
        challenges = resp.json()
        print(f"✅  Challenge.gov: {len(challenges)} competitions fetched")

        return [{
            "title": c.get("title", "")[:255],
            "category": "STEM",
            "description": c.get("brief_description", "")[:500],
            "city": "Washington",
            "state": "DC",
            "country": "US",
            "event_date": (c.get("end_date") or "")[:10],
            "url": f"https://www.challenge.gov/challenge/{c.get('challenge_manager_email', '')}",
            "age_min": 13,
            "age_max": 99,
            "is_virtual": True,
            "source": "challengegov"
        } for c in (challenges if isinstance(challenges, list) else [])]

    except Exception as ex:
        print(f"❌  Challenge.gov failed: {ex}")
        return []

# ─── Seed runner ──────────────────────────────────────────────────────────────

def run_seed():
    db = SessionLocal()

    deleted = db.query(Competition).filter(
        Competition.source.in_(["first_robotics", "eventbrite", "devpost", "challengegov", "sample"])
    ).delete()
    db.commit()
    print(f"🗑️   Cleared {deleted} old rows")

    all_events = fetch_devpost() + fetch_first_robotics() + fetch_challengegov()

    if not all_events:
        print("⚠️  No events fetched from any source")
        db.close()
        return

    for e in all_events:
        comp = Competition(
            title=e["title"],
            category=e["category"],
            description=e.get("description", ""),
            location_city=e["city"],
            location_state=e["state"],
            location_country=e.get("country", "US"),
            event_date=e["event_date"],
            url=e["url"],
            age_min=e.get("age_min"),
            age_max=e.get("age_max"),
            is_virtual=e.get("is_virtual", False),
            source=e["source"]
        )
        db.add(comp)

    db.commit()
    print(f"🎉  Seeded {len(all_events)} real competitions into Talentpedia")
    db.close()

if __name__ == "__main__":
    run_seed()