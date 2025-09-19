from langchain_core.tools import tool
import requests
from app.core.config import URL_CLIENTS
from app.services.busqueda import buscar_documentos
from sentence_transformers.cross_encoder import CrossEncoder
from datetime import datetime
from app.models.schemas import BusquedaRequest

cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

@tool
def buscar_contexto_en_documentos(consulta: str) -> str:
    """Útil para buscar información en documentos. Devuelve el contexto relevante para responder una pregunta."""
    print(f"--- Herramienta RAG buscando contexto para: {consulta} ---")
    
    payload_busqueda = BusquedaRequest(consulta=consulta, top_k=10)
    contexto_chunks = buscar_documentos(payload_busqueda)

    if not contexto_chunks.get('resultados'):
        return "No se encontró contexto relevante en los documentos."
    
    pares_para_rerank = [[consulta, chunk['texto']] for chunk in contexto_chunks['resultados']]
    puntajes = cross_encoder.predict(pares_para_rerank)
    
    for i, chunk in enumerate(contexto_chunks['resultados']):
        chunk['relevance_score'] = puntajes[i]
        
    chunks_reordenados = sorted(contexto_chunks['resultados'], key=lambda x: x['relevance_score'], reverse=True)
    
    contexto_final_chunks = chunks_reordenados[:3]
    
    contexto_str = "".join(chunk['texto'] for chunk in contexto_final_chunks)
    return contexto_str

@tool
def buscar_info_cliente(id: int) -> str:
    """Útil para los detalles de un cliente por su id en el sistema CRM."""
    print(f"--- Herramienta CRM buscando al cliente: {id} ---")
    if not URL_CLIENTS:
        return "Error: La URL del CRM no está configurada en las variables de entorno."
    try:
        response = requests.get(f"{URL_CLIENTS}/{id}")
        response.raise_for_status()
        cliente = response.json()
        if not cliente:
            return f"No se encontró ningún cliente con el id '{id}'."
        return cliente
    except requests.exceptions.RequestException as e:
        return f"Ocurrió un error al contactar la API del CRM: {e}"

@tool
def registrar_cliente(nombre: str, email: str) -> str:
    """Útil para CREAR o REGISTRAR un nuevo cliente. Necesita el nombre y el email."""
    print(f"--- Herramienta: Registrando al cliente: {nombre} ---")
    if not URL_CLIENTS: return "Error: URL_CLIENTS no configurada."
    datos_cliente = {"name": nombre, "email": email, "createdAt": datetime.now().isoformat()}
    try:
        response = requests.post(URL_CLIENTS, json=datos_cliente)
        response.raise_for_status()
        cliente_creado = response.json()
        return f"Cliente '{nombre}' registrado con éxito. Su nuevo ID es {cliente_creado['id']}."
    except requests.exceptions.RequestException as e:
        return f"Error al registrar cliente: {e}"

@tool
def editar_cliente(id: int, nombre: str, email: str) -> str:
    """Útil para ACTUALIZAR o EDITAR un cliente existente. Necesita el ID del cliente y los nuevos datos de nombre y email."""
    print(f"--- Herramienta: Editando al cliente ID: {id} ---")
    if not URL_CLIENTS: return "Error: URL_CLIENTS no configurada."
    url_cliente = f"{URL_CLIENTS}/{id}"
    datos_actualizados = {"name": nombre, "email": email}
    try:
        response = requests.put(url_cliente, json=datos_actualizados)
        response.raise_for_status()
        return f"Cliente con ID {id} actualizado correctamente."
    except requests.exceptions.RequestException as e:
        return f"Error al editar cliente: {e}"

@tool
def eliminar_cliente(id: int) -> str:
    """Útil para BORRAR o ELIMINAR un cliente del sistema. Necesita el ID del cliente."""
    print(f"--- Herramienta: Eliminando al cliente ID: {id} ---")
    if not URL_CLIENTS: return "Error: URL_CLIENTS no configurada."
    url_cliente = f"{URL_CLIENTS}/{id}"
    try:
        response = requests.delete(url_cliente)
        response.raise_for_status()
        return f"Cliente con ID {id} eliminado correctamente."
    except requests.exceptions.RequestException as e:
        return f"Error al eliminar cliente: {e}"