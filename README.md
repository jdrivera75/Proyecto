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