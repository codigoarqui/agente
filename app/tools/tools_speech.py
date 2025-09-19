from langchain_core.tools import tool
import google.generativeai as genai
import os
from app.core.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

@tool
def transcribe_audio_with_gemini(audio_path: str) -> str:
    """
    Útil para transcribir un archivo de audio a texto. Recibe la ruta a un archivo de audio local
    y devuelve el texto contenido en él. Este debe ser el primer paso si el usuario envía una consulta de voz.
    """
    print(f"--- Herramienta de Transcripción transcribiendo audio en: {audio_path} ---")
    try:
        gemini_audio_file = genai.upload_file(path=audio_path)
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        response = model.generate_content(["Transcribe el siguiente audio:", gemini_audio_file])
        
        genai.delete_file(gemini_audio_file.name)
        print(f"Archivo de Gemini eliminado: {gemini_audio_file.name}")

        return response.text
    except Exception as e:
        return f"Error al transcribir el audio: {e}"
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"Archivo de audio temporal eliminado: {audio_path}")
