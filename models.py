# models.py
from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional

# Modelo existente para componentes:
class Component(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    kind: str
    brand: str
    price: float
    description: str
    image_url: str

# Modelo Sugerencia (Ahora con nombre del remitente y URL de imagen opcional):
class Suggestion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sender_name: str # Nombre de la persona que envía la sugerencia
    message: str     # Contenido del comentario
    image_url: Optional[str] = Field(default=None) # URL de la imagen del componente sugerido