from sqlalchemy import Column, Integer, String
from app.db import Base
from pydantic import BaseModel

# --- Modelo ORM (Base de Datos) ---
class LeadORM(Base):
    __tablename__ = "leads"  
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    restaurant_type = Column(String, nullable=False)
    city = Column(String, nullable=False)

# --- Modelo Pydantic (Validación de Búsqueda) ---
class LeadSearchRequest(BaseModel):
    query: str #"Ingrese su consulta aquí"  # Reemplazar con los campos necesarios para la búsqueda