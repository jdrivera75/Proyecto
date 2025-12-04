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


## 🗺️ Endpoints de la API

Esta tabla documenta todas las rutas (endpoints) disponibles en la aplicación, especificando su funcionalidad principal y el tipo de respuesta.

| Ruta (Path) | Método HTTP | Router Principal | Propósito | Tipo de Respuesta |
| :--- | :--- | :--- | :--- | :--- |
| **`/`** | `GET` | `pc_router` | Vista principal del explorador interactivo de la PC Gamer (Renderiza `pc_view.html`). | HTML |
| **`/{component_id}/json`** | `GET` | `components_router` | **Explorador:** Obtiene los detalles de un componente específico (por ID) para ser consumido por JavaScript en el frontend. | JSON |
| **`/{component_id}/delete`** | `POST` | `components_router` | **CRUD:** Elimina un componente de la base de datos (utilizado por un formulario). | Redirección (HTTP 302) |
| **`/submit-contact`** | `POST` | `pc_router` | **Buzón de Sugerencias:** Procesa el envío del formulario, guarda la sugerencia en la DB y maneja la subida de una imagen opcional. | Redirección (HTTP 303) |
| **`/suggestions/json`** | `GET` | `pc_router` | **Buzón:** Obtiene la lista completa de sugerencias recibidas en formato JSON. | JSON |
| **`/suggestions/{suggestion_id}`** | `DELETE` | `pc_router` | **Buzón:** Elimina una sugerencia por ID (diseñado para ser llamado desde JavaScript). | HTTP 204 No Content |