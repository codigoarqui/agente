from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

def generar_embedding(texto: str) -> list[float]:
    return model.encode(texto).tolist()