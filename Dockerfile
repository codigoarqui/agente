FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/code/.cache

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        git \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash appuser

WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /code/.cache && chown -R appuser:appuser /code/.cache

USER appuser
RUN python -c "from sentence_transformers import SentenceTransformer; \
    SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', cache_folder='/code/.cache')"

USER root
COPY ./app /code/app
RUN chown -R appuser:appuser /code/app

EXPOSE 7860

USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
# uvicorn app.main:app --host 0.0.0.0 --port 7860"