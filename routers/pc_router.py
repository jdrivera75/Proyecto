from fastapi import APIRouter, Request, Depends, Form, status, UploadFile, File, Response 
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from database import get_session
from models import Component, Suggestion 
from typing import Optional

import shutil
import os
import uuid 

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Directorio donde se guardarán las imágenes de las sugerencias
STATIC_DIR = "static/img/suggested_components" 

@router.get("/", response_class=HTMLResponse, name="pc_interactive_view")
def pc_interactive_view(request: Request, session: Session = Depends(get_session)):
    components = session.exec(select(Component).limit(5)).all()
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
    
    # Lógica de manejo y guardado de archivos
    if component_image and component_image.filename and component_image.size > 0:
        file_extension = os.path.splitext(component_image.filename)[1]
        
        # Usamos un UUID para un nombre de archivo único y seguro
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        file_path = os.path.join(STATIC_DIR, unique_filename)

        try:
            # 1. Crear el directorio si no existe
            os.makedirs(STATIC_DIR, exist_ok=True) 
            # 2. Guardar el archivo en el sistema de archivos
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(component_image.file, buffer)
            # 3. Guardar la URL pública en la base de datos
            image_url_db = f"/static/img/suggested_components/{unique_filename}"
        except Exception as e:
            print(f"Error al guardar la imagen de sugerencia: {e}")
        finally:
            # Es importante cerrar el archivo subido
            component_image.file.close()


    new_suggestion = Suggestion(
        sender_name=sender_name,
        message=suggestion_message,
        image_url=image_url_db 
    )
    session.add(new_suggestion)
    session.commit()
    session.refresh(new_suggestion)
    print(f"Sugerencia de {sender_name} guardada con ID: {new_suggestion.id}")

    # Establecer la cookie de éxito
    response = RedirectResponse(
        url=request.url_for("pc_interactive_view"), 
        status_code=status.HTTP_303_SEE_OTHER
    )
    # Se añade la cookie para mostrar el mensaje de éxito en la vista principal
    response.set_cookie(key="success_message", value="¡Sugerencia enviada con éxito!", httponly=False)
    return response


# RUTA GET: OBTENER SUGERENCIAS EN FORMATO JSON
@router.get("/suggestions/json")
def get_suggestions_json(session: Session = Depends(get_session)):
    suggestions = session.exec(select(Suggestion)).all()
    
    return [
        {
            "id": s.id, 
            "sender_name": s.sender_name, 
            "message": s.message, 
            "image_url": s.image_url # Clave para el frontend
        } 
        for s in suggestions
    ]


@router.delete("/suggestions/{suggestion_id}")
def delete_suggestion(suggestion_id: int, session: Session = Depends(get_session)):
    """Elimina una sugerencia por ID."""
    suggestion = session.get(Suggestion, suggestion_id)
    if suggestion:
        session.delete(suggestion)
        session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)