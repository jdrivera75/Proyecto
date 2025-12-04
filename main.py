# main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# 1. Importar los módulos necesarios
from database import create_db_and_tables 
from routers import pc_router, components_router 

# ===========================================
# 2. INICIALIZACIÓN DE FASTAPI
# ===========================================
app = FastAPI(
    title="PC Builder Interactivo",
    description="Aplicación web para visualizar y gestionar componentes de PC y un Buzón de Sugerencias con nombre.",
    version="1.0.0",
)

# ===========================================
# 3. CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS
# ===========================================
app.mount("/static", StaticFiles(directory="static"), name="static")

# ===========================================
# 4. INCLUSIÓN DE ROUTERS
# ===========================================
app.include_router(pc_router.router, tags=["PC"])
app.include_router(components_router.router, prefix="/components", tags=["Components"])



@app.on_event("startup")
def on_startup():
    """Crea la base de datos y las tablas al iniciar la aplicación."""
    create_db_and_tables() 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)