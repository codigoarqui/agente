from google import genai
from google.genai import types
from markdown import markdown
from bs4 import BeautifulSoup
import wave
from app.core.config import GEMINI_API_KEY

def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Guarda los bytes PCM en un archivo WAV."""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

def text_to_speech(text: str, file_name: str = "out.wav") -> str:
    """
    Convierte texto a audio WAV usando Gemini 2.5 TTS.
    """
    html = markdown(text)
    soup = BeautifulSoup(html, "html.parser")
    plain_text = soup.get_text()

    print(f"Generando audio con Gemini para: '{plain_text[:70]}...'")

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=plain_text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name="Kore"
                        )
                    )
                ),
            ),
        )

        audio_bytes = response.candidates[0].content.parts[0].inline_data.data
        wave_file(file_name, audio_bytes)

    except Exception as e:
        print(f"Error al generar audio con Gemini: {e}")
        raise Exception("Error al generar el audio con Gemini.")