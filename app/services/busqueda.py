from app.core.embedding import generar_embedding
from app.core.supabase_client import supabase
from app.models.schemas import BusquedaRequest

def buscar_documentos(payload: BusquedaRequest):
    vector = generar_embedding(payload.consulta)

    resultado = supabase.rpc(
        "buscar_similares",
        {"query": vector, "top_k": payload.top_k}
    ).execute()

    return {"resultados": resultado.data}