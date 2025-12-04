# database.py
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

DATABASE_URL = "sqlite:///./pcbuilder.db"
# Desactivamos check_same_thread para SQLite, típico en FastAPI
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables() -> None:
    # Se crea la base de datos y las tablas si no existen
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    # Dependencia para manejar sesiones de DB
    with Session(engine) as session:
        yield session

# Función para obtener la engine si la necesitamos externamente (ej. seed_data)
def get_engine():
    return engine