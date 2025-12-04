Contenido del Archivo README.md


#  PC Builder Interactivo (FastAPI + SQLModel + Jinja)

Proyecto de aplicación web interactiva desarrollada con **FastAPI** que simula el montaje de una PC Gamer, permitiendo a los usuarios interactuar con componentes y enviar sugerencias a través de un buzón con gestión de archivos y base de datos.

Este proyecto sigue una arquitectura MVC ligera, utilizando SQLModel para la gestión de datos persistentes (SQLite).

##  Características Principales

* **Explorador Interactivo:** Visualización de la torre de PC con botones flotantes que muestran detalles (nombre, marca, precio, descripción) de cada componente al hacer clic.
* **Gestión de Componentes (CRUD):** Las rutas `/components` permiten listar, crear, ver detalles y eliminar componentes.
* **Buzón de Sugerencias:** Formulario unificado que permite a los usuarios enviar comentarios con su nombre, correo y, opcionalmente, cargar una imagen para el componente sugerido.
* **Gestión de Sugerencias:** Modal para visualizar todas las sugerencias recibidas con la opción de **eliminación** (`DELETE`) controlada desde el *frontend* con JavaScript.
* **Arquitectura:** Organización del código modular en routers (`pc_router.py`, `components_router.py`) para mantener la aplicación escalable y limpia.
* **Despliegue:** Preparado para desplegar en servicios de cloud como Render.

este es el link para abrir el render:
https://proyecto-rx73.onrender.com




| Tecnología | Descripción |
| :--- | :--- |
| **Backend** | FastAPI (Python) |
| **Base de Datos** | SQLModel (ORM) + SQLite |
| **Servidor Web** | Uvicorn |
| **Frontend** | HTML5, CSS3, Jinja2 Templates, JavaScript |


Ruta (Path),Método HTTP,Router,Propósito,Tipo de Respuesta
/,GET,pc_router,Muestra la página de inicio interactiva (pc_view.html) y consulta los componentes principales.,HTML
---,---,---,---,---
/{component_id}/json,GET,components_router,"Explorador Interactivo: Obtiene los detalles de un componente específico (por ID) en formato JSON, con lógica para sobrescribir algunas URLs de imagen.",JSON (Detalles del Componente)
/{component_id}/delete,POST,components_router,CRUD: Elimina un componente de la base de datos (se usa POST y RedirectResponse para formularios HTML tradicionales).,Redirección a /components
---,---,---,---,---
/submit-contact,POST,pc_router,"Buzón de Sugerencias: Procesa el envío del formulario de contacto/sugerencias, guarda el texto y opcionalmente sube y guarda la imagen en el servidor.",Redirección a /
/suggestions/json,GET,pc_router,Obtiene todas las sugerencias de la base de datos en formato JSON (utilizado por el frontend para mostrar las sugerencias en un modal).,JSON (Lista de Sugerencias)
/suggestions/{suggestion_id},DELETE,pc_router,Gestión de Sugerencias: Elimina una sugerencia por ID de la base de datos. Está diseñado para ser llamado vía JavaScript desde el frontend.,HTTP 204 No Content