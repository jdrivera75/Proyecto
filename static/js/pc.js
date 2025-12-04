// static/js/pc.js
document.addEventListener("DOMContentLoaded", function () {
    const pcImg = document.getElementById("pc-main");
    const componentPanel = document.getElementById("component-panel");
    const closePanelBtn = document.getElementById("close-panel");
    const contactModal = document.getElementById("contact-modal");
    const openContactBtn = document.getElementById("open-contact-btn");
    const closeModalBtn = document.querySelector(".close-modal");
    
    const openSuggestionsBtn = document.getElementById("open-suggestions-btn");
    const suggestionsModal = document.getElementById("suggestions-modal");
    const closeSuggestionsModalBtn = document.querySelector(".close-suggestions-modal");

    // --- Funciones de Fallback y Componentes ---
    function getFallbackImageUrl(componentId) {
        // ... (Tu lógica existente de fallback)
        switch (componentId.toString()) { 
            case '2': return '/static/img/grafica.webp';
            case '3': return '/static/img/What-Is-a-Core-in-a-CPU.jpg';
            case '7': return '/static/img/RamPC-Ramlaptop-640.jpg';
            case '4': return '/static/img/motherboard-683247_1280.webp';
            case '5': return '/static/img/fuente.png';
            case '6': return '/static/img/SSD-i8kf.webp';
            case '8': return '/static/img/ventiladores.jpg';
            default: return 'https://placehold.co/400x180/121212/ff3366?text=No+Image';
        }
    }

    async function loadComponent(id) { 
        try {
            const res = await fetch('/components/' + id + '/json');
            if (!res.ok) {
                throw new Error(`Error cargando componente (Status: ${res.status}).`);
            }
            const data = await res.json();
            openPanelWithData(data, id); 
        } catch (err) {
            console.error(err);
            alert(`ERROR: No se pudo cargar el componente (ID: ${id}).\n\nVerifica si la base de datos (pcbuilder.db) está cargada con datos iniciales (seed_data).`);
        }
    }

    function openPanelWithData(data, componentId) { 
        if (componentPanel.classList.contains("open")) closePanel(); 

        let imagePath;
        if (data.image_url && typeof data.image_url === 'string' && data.image_url.trim() !== "" && data.image_url !== 'N/A') {
            imagePath = data.image_url.startsWith('/') ? data.image_url : '/static/img/' + data.image_url;
        } else {
            imagePath = getFallbackImageUrl(componentId);
        }
        document.getElementById("comp-img").src = imagePath;

        document.getElementById("comp-name").innerText = data.name || "Componente Desconocido";
        document.getElementById("comp-kind").innerText = "Tipo: " + (data.kind || "—");
        document.getElementById("comp-brand").innerText = "Marca: " + (data.brand || "—");
        document.getElementById("comp-price").innerText =
            "Precio: $" + (data.price !== undefined ? Number(data.price).toFixed(2) : "N/A");
        document.getElementById("comp-desc").innerText = data.description || "Sin descripción disponible.";
        
        componentPanel.classList.add("open");
        pcImg.style.transition = "transform 0.5s ease-in-out";
        pcImg.style.transform = "scale(1.35)"; 
    }


    function closePanel() {
        componentPanel.classList.remove("open");
        pcImg.style.transform = ""; 
        pcImg.style.transition = "transform 0.4s ease";
    }

    function openModal() { contactModal.style.display = "block"; }
    function closeModal() { contactModal.style.display = "none"; }

    // Función para manejar el cierre al hacer click fuera o con tecla Escape
    window.onclick = function(event) {
        if (event.target == contactModal) {
            closeModal();
        }
        if (event.target == suggestionsModal) {
            suggestionsModal.style.display = "none";
        }
    }
    window.onkeydown = function(event) {
        if (event.key === 'Escape') {
            closeModal();
            closePanel();
            suggestionsModal.style.display = "none";
        }
    }
    
    // --- EVENT LISTENERS ---
    document.querySelectorAll('.component-button[data-id]').forEach(button => {
        button.addEventListener('click', async (e) => {
            e.preventDefault();
            if (contactModal.style.display === "block" || suggestionsModal.style.display === "block") return;
            const id = button.dataset.id;
            await loadComponent(id); 
        });
    });

    closePanelBtn?.addEventListener("click", () => closePanel());
    openContactBtn?.addEventListener('click', () => { closePanel(); openModal(); });
    closeModalBtn?.addEventListener('click', () => closeModal());
    
    openSuggestionsBtn?.addEventListener('click', () => {
        closePanel(); 
        closeModal();
        loadSuggestions(); // Carga de datos
        suggestionsModal.style.display = "block";
    });

    closeSuggestionsModalBtn?.addEventListener('click', () => {
        suggestionsModal.style.display = "none";
    });
    
    // 🌟 FUNCIÓN: Eliminar sugerencia 🌟
    async function deleteSuggestion(id) {
        if (!confirm("¿Estás seguro de que deseas eliminar esta sugerencia?")) return;

        try {
            const res = await fetch(`/suggestions/${id}`, {
                method: 'DELETE',
            });

            if (res.status === 204) { 
                alert("Sugerencia eliminada con éxito.");
                loadSuggestions(); 
            } else {
                alert(`Error al eliminar la sugerencia. Código: ${res.status}.`); 
            }
        } catch (err) {
            console.error("Fallo al intentar eliminar la sugerencia:", err);
            alert("Error de conexión al eliminar la sugerencia.");
        }
    }
    
    // 🌟 FUNCIÓN: Cargar las sugerencias (CON IMAGEN DE PERFIL) 🌟
    async function loadSuggestions() {
        const listDiv = document.getElementById("suggestions-list");
        listDiv.innerHTML = '<p>Cargando sugerencias...</p>'; 

        try {
            const res = await fetch('/suggestions/json');
            if (!res.ok) {
                listDiv.innerHTML = '<p style="color:red;">Error al cargar sugerencias.</p>';
                return;
            }
            const data = await res.json();
            
            if (data.length === 0) {
                listDiv.innerHTML = '<p>El buzón está vacío. ¡Sé el primero en dejar un comentario!</p>';
                return;
            }
            
            listDiv.innerHTML = data.map(s => {
                // 🌟 LÓGICA CLAVE PARA MOSTRAR LA IMAGEN DE PERFIL (Redonda)
                let imageHtml = '';
                if (s.image_url) {
                    imageHtml = `
                        <div style="flex-shrink: 0; text-align: center;">
                            <img src="${s.image_url}" 
                                 alt="Foto de perfil de ${s.sender_name}" 
                                 style="width: 70px; height: 70px; border-radius: 50%; object-fit: cover; border: 2px solid #00bfff;">
                        </div>
                    `;
                } else {
                    // Placeholder para cuando no hay imagen
                    imageHtml = `
                        <div style="flex-shrink: 0; width: 70px; height: 70px; background: #333; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2em; color: #aaa;">
                            👤
                        </div>
                    `;
                }
                // ---------------------------------------------
                
                return `
                    <div class="suggestion-item" style="border-bottom: 1px dashed #444; padding: 10px 0; position: relative; margin-bottom: 10px; display: flex; align-items: flex-start; gap: 15px;">
                        
                        ${imageHtml}
                        
                        <div style="flex-grow: 1; min-width: 0;">
                            <p style="margin: 0; color: #fff; word-wrap: break-word;">
                                💬 <strong>${s.sender_name || 'Usuario Desconocido'} dice:</strong> 
                                ${s.message}
                            </p>
                            <p style="font-size: 0.8em; opacity: 0.6; margin-top: 5px;">Comentario ID: ${s.id}</p>
                        </div>
                        
                        <button class="delete-suggestion-btn" data-id="${s.id}" 
                                style="position: absolute; top: 5px; right: 5px; background: none; border: 1px solid red; color: red; cursor: pointer; padding: 3px 6px; border-radius: 5px; font-size: 10px;">
                            ✕ Eliminar
                        </button>
                    </div>`;
            }).join('');

            // Re-asignar eventos de eliminación después de actualizar el HTML
            document.querySelectorAll('.delete-suggestion-btn').forEach(button => {
                const id = parseInt(button.dataset.id);
                button.addEventListener('click', () => deleteSuggestion(id));
            });

        } catch (err) {
            console.error("Error al cargar sugerencias:", err);
            listDiv.innerHTML = '<p style="color:red;">Fallo de conexión al cargar el buzón.</p>';
        }
    }

    // --- Lógica de mensaje de éxito ---
    const successMessageDiv = document.querySelector('.success-message');
    if (successMessageDiv) {
        // Eliminar la cookie después de 3 segundos para que no vuelva a aparecer
        setTimeout(() => {
            document.cookie = "success_message=; Max-Age=0; path=/"; 
            successMessageDiv.remove();
        }, 3000); 
    }

});