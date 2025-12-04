
from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional

class Component(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    kind: str
    brand: str
    price: float
    description: str
    image_url: str

class Suggestion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sender_name: str 
    message: str     
    image_url: Optional[str] = Field(default=None) 