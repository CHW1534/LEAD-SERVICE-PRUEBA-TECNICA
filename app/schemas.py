from sqlalchemy import Column, Integer, String
from app.db import Base
from pydantic import BaseModel



# Modelo ORM para la tabla "leads" en la base de datos
class LeadORM(Base):
    # Nombre real de la tabla en la BD
    __tablename__ = "leads"  
    # Definición de columnas
    id = Column(Integer, primary_key=True, index=True)  # ID autoincremental
    name = Column(String, nullable=False)               # Nombre obligatorio
    email = Column(String, nullable=False)              # Email obligatorio
    phone = Column(String, nullable=False)              # Teléfono
    restaurant_type = Column(String, nullable=False)    # Tipo de comida (Mariscos, Tacos, etc.)
    city = Column(String, nullable=False)               # Ciudad
    


class LeadSearchRequest(BaseModel):
    query: str


