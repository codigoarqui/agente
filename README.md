---
title: Agente Conversacional Multimodal
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Agente Conversacional Multimodal con FastAPI, LangGraph y Gemini

Este proyecto, creado para el canal de YouTube **[Del Código a la Arquitectura](https://www.youtube.com/@CodigoArquitectura)**, implementa un agente de IA conversacional avanzado capaz de procesar texto, voz e imágenes.

El backend está construido con **FastAPI** y utiliza **LangGraph** para orquestar la lógica del agente, que se apoya en los modelos de **Google Gemini** para sus capacidades multimodales.

---

## 🚀 Características Principales

-   **Backend con FastAPI**: Expone la lógica del agente a través de una API REST robusta y rápida.
-   **Orquestación con LangGraph**: Gestiona flujos de conversación complejos y la ejecución de herramientas de forma inteligente.
-   **Capacidades Multimodales**:
    -   **Texto**: Procesamiento de consultas en formato de texto.
    -   **Voz**: Transcripción de audio a texto y conversión de texto a voz (TTS) para respuestas audibles.
    -   **Visión**: Análisis de imágenes para responder preguntas sobre su contenido.
-   **Arquitectura Basada en Herramientas**: El agente puede usar un conjunto de herramientas extensibles para:
    -   Realizar búsquedas semánticas en una base de datos vectorial.
    -   Consultar, registrar, editar y eliminar información de clientes.
-   **Memoria Persistente**: Utiliza **Supabase (PostgreSQL)** para almacenar el historial de conversaciones, permitiendo un diálogo continuo y contextual.
-   **Búsqueda Semántica**: Integrado como una herramienta, utiliza `pgvector` para encontrar información relevante en una base de datos de documentos.
-   **Dockerizado**: Listo para un despliegue sencillo en plataformas como **Hugging Face Spaces**.

---

## 🏗️ Arquitectura del Proyecto

-   `app/main.py`: Punto de entrada de la aplicación FastAPI.
-   `app/routes/agent.py`: Contiene el endpoint principal `/agent/` que recibe las peticiones y orquesta la respuesta del agente.
-   `app/tools/`: Módulos con las funciones que el agente puede ejecutar (búsqueda, visión, gestión de clientes).
-   `app/services/`: Servicios auxiliares, como el `tts_service` para la conversión de texto a voz.
-   `app/core/`: Contiene la configuración central, el cliente de Supabase y la gestión de la memoria del chat.
-   `app/models/`: Define los esquemas de datos (Pydantic) para las peticiones y respuestas.

---

## 🛠️ Configuración del Entorno

### 1. Clonar el Repositorio

```bash
git clone https://github.com/codigoarqui/agente.git
cd agente
```

### 2. Configurar Supabase

Necesitarás una cuenta en [Supabase](https://supabase.com). Una vez creado tu proyecto, ejecuta los siguientes scripts en el **SQL Editor**:

1.  **Activar la extensión `pgvector`**:
    ```sql
    create extension if not exists vector;
    ```

2.  **Crear la tabla para búsqueda semántica**: Almacena los embeddings de documentos. El vector debe ser de 384 dimensiones para el modelo `paraphrase-multilingual-MiniLM-L12-v2`.
    ```sql
    create table documentos (
      id uuid primary key default gen_random_uuid(),
      texto text,
      metadatos jsonb,
      embedding vector(384)
    );
    ```

3.  **Crear la función para búsqueda semántica**:
    ```sql
    create or replace function buscar_similares(query vector(384), top_k int)
    returns table(id uuid, texto text, metadatos jsonb)
    language sql stable
    as $$
      select id, texto, metadatos
      from documentos
      order by embedding <-> query
      limit top_k;
    $$;
    ```

4.  **Crear la tabla para el historial de chat**:
    ```sql
    CREATE TABLE public.historial_chat (
      session_id TEXT PRIMARY KEY,
      historial JSONB,
      updated_at TIMESTAMPTZ DEFAULT NOW()
    );
    ```

### 3. Configurar Variables de Entorno

Crea un archivo `.env` a partir del ejemplo `.env.example` y añade tus credenciales:

```ini
# Credenciales de Supabase
SUPABASE_URL="https://tu-proyecto.supabase.co"
SUPABASE_KEY="tu-api-key-anon"

# API Key de Google Gemini (Google AI Studio)
GEMINI_API_KEY="tu-gemini-api-key"

# URL para la herramienta de gestión de clientes
URL_CLIENTS="https://url-de-tu-api-de-clientes"
```

### 4. Instalar Dependencias

Crea un entorno virtual y activa las dependencias desde `requirements.txt`.

```bash
# Crear y activar entorno virtual (ej. en macOS/Linux)
python3 -m venv venv
source venv/bin/activate
```

```bash
# Crear y activar entorno virtual (ej. en Windows)
python3 -m venv venv
venv\Scripts\activate
```

```bash
# Instalar librerías
pip install -r requirements.txt
```

---

## ▶️ Ejecutar Localmente

Con el entorno configurado, inicia el servidor de FastAPI:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`. Puedes ver la documentación interactiva de Swagger en `http://localhost:8000/docs`.

---

## 🚀 Despliegue en Hugging Face

1.  Crea un nuevo **Space** en [Hugging Face](https://huggingface.co/new-space).
2.  Selecciona **Docker** como el SDK del Space.
3.  Elige la plantilla "Blank" o una apropiada.
4.  Vincula tu repositorio de GitHub.
5.  En la configuración del Space (`Settings`), ve a la sección de **Secrets** y añade las variables de entorno (`SUPABASE_URL`, `SUPABASE_KEY`, `GEMINI_API_KEY`, `URL_CLIENTS`).
6.  Hugging Face construirá y desplegará automáticamente la aplicación usando el `Dockerfile` del repositorio.

---

## 🔍 Uso de la API

El endpoint principal es `POST /agent/`. Acepta un cuerpo JSON con el siguiente formato:

```json
{
  "consulta": "Hola, ¿quién eres?",
  "session_id": "user123",
  "audio_base64": null,
  "image_base64": null
}
```

-   `consulta`: El texto de la pregunta (opcional si se envía audio).
-   `session_id`: Un identificador único para mantener el historial de la conversación.
-   `audio_base64`: Un string con el audio codificado en Base64 (opcional).
-   `image_base64`: Un string con la imagen codificada en Base64 (opcional).

#### Respuestas

-   Si la petición es de texto o imagen, la respuesta será un JSON:
    ```json
    {
      "respuesta": "Soy un asistente de IA...",
      "contexto": []
    }
    ```
-   Si la petición incluye audio (`audio_base64`), la respuesta será un **archivo de audio** (`audio/wav`) con la voz del agente.

---

Si este proyecto te ha sido útil, no olvides suscribirte al canal **Del Código a la Arquitectura**. ¡Nos vemos en el próximo vídeo! 🚀