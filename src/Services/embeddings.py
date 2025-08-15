import os
from sentence_transformers import SentenceTransformer

_model = None
def get_embedding_model():
    global _model
    if _model is None:
        model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        _model = SentenceTransformer(model_name)
    return _model

def embedding_dim():
    return get_embedding_model().get_sentence_embedding_dimension()

def get_embedding(text: str):
    model = get_embedding_model()
    return model.encode(text).tolist()