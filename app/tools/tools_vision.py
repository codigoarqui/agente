from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from app.core.config import GEMINI_API_KEY
import os
import base64

@tool
def analyze_image_with_gemini_vision(user_prompt:str, image_path: str) -> str:
    """
    Analiza el contenido de una imagen ubicada en la ruta (image_path) y devuelve una descripción segun el texto que el usuario envió como prompt.
    Esta herramienta es el primer paso para responder cualquier pregunta sobre una imagen.
    Debe ser invocada antes de intentar responder a una pregunta que involucre una imagen.
    """
    print(f"--- Herramienta de Visión describiendo imagen en: {image_path} ---")
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GEMINI_API_KEY)

        with open(image_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")

        message = HumanMessage(
            content=[
                {"type": "text", "text": user_prompt},
                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_base64}"},
            ]
        )

        response = llm.invoke([message])

        if isinstance(response.content, str):
            return response.content
        if isinstance(response.content, list):
            return " ".join(str(part) for part in response.content)

        return str(response.content)
    except Exception as e:
        return f"Error al analizar la imagen desde la ruta {image_path}: {e}"
    finally:
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
                print(f"Archivo eliminado: {image_path}")
        except Exception as del_error:
            print(f"No se pudo eliminar {image_path}: {del_error}")