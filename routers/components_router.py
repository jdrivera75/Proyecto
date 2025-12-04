# routers/components_router.py
from fastapi import APIRouter, Request, Form, Depends, HTTPException, status 
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from database import get_session
from sqlmodel import Session
# Importación directa
from models import Component 

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/{component_id}/json")
def component_json(component_id: int, session: Session = Depends(get_session)):
    comp = session.get(Component, component_id)
    
    if not comp:
        raise HTTPException(status_code=404, detail="Componente no encontrado en la DB")

    image_url_final = comp.image_url
    
    if comp.id == 2: # Tarjeta Gráfica
        image_url_final = "/static/img/grafica.webp"
    elif comp.id == 8: # Ventiladores
        image_url_final = "/static/img/ventiladores.jpg"
    elif comp.id == 5: # Fuente de Poder
        image_url_final = "/static/img/fuente.png"
    
    return {
        "id": comp.id,
        "name": comp.name,
        "kind": comp.kind,
        "brand": comp.brand,
        "price": comp.price,
        "description": comp.description,
        "image_url": image_url_final 
    }
    

@router.post("/{component_id}/delete")
def delete_component(component_id: int, session: Session = Depends(get_session)):
    comp = session.get(Component, component_id)
    if not comp:
        raise HTTPException(404, "Componente no encontrado")

    session.delete(comp)
    session.commit()
    return RedirectResponse("/components", status_code=status.HTTP_302_FOUND)