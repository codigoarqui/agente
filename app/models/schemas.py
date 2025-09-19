from typing import Dict

from pydantic import BaseModel


class DocumentoRequest(BaseModel):
    texto: str
    metadatos: Dict = {}

from typing import Optional

class BusquedaRequest(BaseModel):
    consulta: str
    session_id: str = ''
    top_k: int = 3
    image_base64: Optional[str] = None
    audio_base64: Optional[str] = None