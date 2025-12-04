from sqlmodel import Session
from models import Component
from database import get_engine

def create_default_components():
    engine = get_engine()
    
    # 1. Borrar componentes existentes para evitar duplicados en cada ejecución
    with Session(engine) as session:
        # Usa .delete() en la consulta directamente para ser más eficiente en SQLModel
        session.query(Component).delete() 
        session.commit()
    
    # IDs 2, 3, 4, 5, 6, 7, 8 son los definidos en pc_view.html
    components_to_create = [
        # Componente 2 (GPU)
        Component(
            id=2, 
            name="Tarjeta Gráfica RTX 4070", 
            kind="GPU", 
            brand="NVIDIA", 
            price=600.00, 
            description="Procesa gráficos a alta velocidad para juegos 4K y ray-tracing.", 
            image_url="/static/img/tarjeta-grafica-que-es-para-que-sirve-co....jpg" 
        ),
        # Componente 3 (CPU)
        Component(
            id=3, 
            name="Procesador Core i9-14900K", 
            kind="CPU", 
            brand="Intel", 
            price=550.00, 
            description="El núcleo de la PC, esencial para el rendimiento multitarea.", 
            image_url="/static/img/What-Is-a-Core-in-a-CPU.jpg"
        ),
        # Componente 4 (Motherboard)
        Component(
            id=4, 
            name="Placa Base ROG Strix Z790", 
            kind="Motherboard", 
            brand="ASUS", 
            price=300.00, 
            description="Plataforma central con soporte para DDR5 y PCIe 5.0.", 
            image_url="/static/img/motherboard-683247_1280.webp"
        ),
        # Componente 5 (PSU)
        Component(
            id=5, 
            name="Fuente de Poder 1000W 80+ Gold", 
            kind="PSU", 
            brand="Corsair", 
            price=150.00, 
            description="Suministra energía estable y eficiente a todos los componentes.", 
            image_url="/static/img/FUENTE-DE-PODER-PC-300W_80326_JAL.jpg"
        ),
        # Componente 6 (Storage - SSD)
        Component(
            id=6, 
            name="SSD NVMe 2TB Gen4", 
            kind="Storage", 
            brand="Samsung", 
            price=120.00, 
            description="Unidad de estado sólido ultrarrápida para cargar juegos en segundos.", 
            image_url="/static/img/SSD-i8kf.webp"
        ),
        # Componente 7 (RAM - NUEVO)
        Component(
            id=7, 
            name="Memoria RAM DDR5 32GB (2x16GB)", 
            kind="RAM", 
            brand="G.Skill Trident Z5 RGB", 
            price=180.00, 
            description="Memoria de acceso rápido con iluminación RGB sincronizable.", 
            image_url="/static/img/RamPC-Ramlaptop-640.jpg" # Usa tu imagen de RAM aquí
        ),
        # Componente 8 (COOLING - NUEVO)
        Component(
            id=8, 
            name="Kit de Ventiladores RGB (3-pack)", 
            kind="Cooling", 
            brand="Cooler Master", 
            price=60.00, 
            description="Mantiene la temperatura baja con flujo de aire optimizado y luces RGB.", 
            image_url="/static/img/633e516c5d043305d331607b-alsey-pc-f...webp" # Usa tu imagen de Ventiladores aquí
        ),
    ]

    with Session(engine) as session:
        for comp in components_to_create:
            session.add(comp)
        session.commit()
    print("Datos semilla (seed data) cargados exitosamente con IDs 7 y 8.")

if __name__ == "__main__":
    from database import create_db_and_tables
    create_db_and_tables() 
    create_default_components()