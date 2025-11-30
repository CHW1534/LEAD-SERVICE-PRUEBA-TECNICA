from pydantic import BaseModel, EmailStr, Field, constr, conint, validator

# Modelo para RECIBIR datos (Input) ---
class LeadCreate(BaseModel):
 # Datos necesarios para crear un nuevo lead
    name: str
    email: EmailStr  # Valida que tenga formato de correo sea válido
    phone: str
    restaurant_type: str
    city: str

# Modelo para RESPONDER datos (Output) ---
class LeadResponse(LeadCreate):
    
    id: int

# permite a Pydantic leer datos directamente de un objeto ORM de SQLAlchemy

    class Config:
            from_attributes = True
            
# Modelo para recibir la consulta de búsqueda
class LeadRequest(BaseModel):
    name: str
    city: str
    type: str