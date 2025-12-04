# routers/pc_router.py
from fastapi import APIRouter, Request, Depends, Form, status, UploadFile, File, HTTPException, Response # 👈 Importar Response
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from database import get_session
# Importación directa
from models import Component, Suggestion 
from typing import Optional

import shutil
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

STATIC_DIR = "static/img/suggested_components" 

@router.get("/", response_class=HTMLResponse)
def pc_interactive_view(request: Request, session: Session = Depends(get_session)):
    components = session.query(Component).limit(5).all()
    build = {"name": "PC Gamer Elite", "description": "Explorador Interactivo de Componentes."}
    return templates.TemplateResponse(
        "pc_view.html", 
        {"request": request, "build": build, "components": components}
    )

@router.post("/submit-contact")
def submit_contact(
    request: Request,
    sender_name: str = Form(..., alias="name"), 
    email: str = Form(...),
    suggestion_message: str = Form(..., alias="suggestion_box"), 
    component_image: Optional[UploadFile] = File(None), 
    session: Session = Depends(get_session)
):
    image_url_db = None
    if component_image and component_image.filename:
        file_extension = os.path.splitext(component_image.filename)[1]
        unique_filename = f"suggest_{sender_name.replace(' ', '_').lower()}_{os.urandom(4).hex()}{file_extension}"
        file_path = os.path.join(STATIC_DIR, unique_filename)

        try:
            os.makedirs(STATIC_DIR, exist_ok=True) 
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(component_image.file, buffer)
            image_url_db = f"/static/img/suggested_components/{unique_filename}"
        except Exception as e:
            print(f"Error al guardar la imagen de sugerencia: {e}")

    new_suggestion = Suggestion(
        sender_name=sender_name,
        message=suggestion_message,
        image_url=image_url_db
    )
    session.add(new_suggestion)
    session.commit()
    print(f"Sugerencia de {sender_name} guardada.")

    return RedirectResponse(
        url="/", 
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/suggestions/json")
def get_suggestions_json(session: Session = Depends(get_session)):
    suggestions = session.query(Suggestion).all()
    
    return [
        {"id": s.id, "sender_name": s.sender_name, "message": s.message, "image_url": s.image_url} 
        for s in suggestions
    ]

# ===============================================
# RUTA DELETE: ELIMINAR SUGERENCIA (USANDO RESPONSE PARA FORZAR 204)
# ===============================================
@router.delete("/suggestions/{suggestion_id}")
def delete_suggestion(suggestion_id: int, session: Session = Depends(get_session)):
    """Elimina una sugerencia por ID y devuelve 204 (No Content)."""
    suggestion = session.get(Suggestion, suggestion_id)
    
    if suggestion:
        session.delete(suggestion)
        session.commit()
    
    # 🌟 CORRECCIÓN APLICADA: Devolvemos una respuesta vacía con el código 204
    return Response(status_code=status.HTTP_204_NO_CONTENT)