from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import dotenv
dotenv.load_dotenv()

from app.db import engine, Base, get_db
from app.models import LeadCreate, LeadResponse
from app.schemas import LeadORM
from app.services.api_client import fetch_city_info
from app.services.vector_service import embed, similarity


# --- Inicializar base de datos ---
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Microservicio de Leads de Restaurantes")
# ---------------------------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------------------------

@app.get("/health")
def health_check():
    return {"status": "ok"}

# ---------------------------------------------------------------------------
# CREAR LEAD
# ---------------------------------------------------------------------------

@app.post("/api/leads/", response_model=LeadResponse)
async def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    city_info = await fetch_city_info(lead.city)
    print(f"[INFO] External city info for '{lead.city}': {city_info}")

    db_lead = LeadORM(**lead.dict())

    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)

    return db_lead

# ---------------------------------------------------------------------------
# LISTAR LEADS
# ---------------------------------------------------------------------------

@app.get("/api/leads/", response_model=list[LeadResponse])
def read_leads(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(LeadORM).offset(skip).limit(limit).all()

# ---------------------------------------------------------------------------
#  calcular similitud de texto para un lead
# ---------------------------------------------------------------------------

def compute_lead_score(lead: LeadORM, query: str) -> float:
    import difflib

    q = query.lower()

    w_city = 0.6
    w_type = 0.3
    w_name = 0.1

    score_city = difflib.SequenceMatcher(None, lead.city.lower(), q).ratio()
    score_type = difflib.SequenceMatcher(None, lead.restaurant_type.lower(), q).ratio()
    score_name = difflib.SequenceMatcher(None, lead.name.lower(), q).ratio()

    return (
        score_city * w_city +
        score_type * w_type +
        score_name * w_name
    )


# ---------------------------------------------------------------------------
# BÚSQUEDA POR SIMILITUD
# ---------------------------------------------------------------------------
@app.post("/api/leads/search", response_model=list[LeadResponse])
def search_leads(payload: dict, db: Session = Depends(get_db)):
    search_query = payload.get("query")
    if not search_query:
        raise HTTPException(status_code=400, detail="Query is required")

    all_leads = db.query(LeadORM).all()

# Calcular puntuaciones de similitud
    scored_leads = [
        {"lead": lead, "score": compute_lead_score(lead, search_query)}
        for lead in all_leads
    ]
    
    scored_leads.sort(key=lambda x: x["score"], reverse=True)
    return [item["lead"] for item in scored_leads]
