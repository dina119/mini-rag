import os
import torch
print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU")
from sentence_transformers import SentenceTransformer
import time
_device = "cuda" if torch.cuda.is_available() else "cpu"
_model = None
def get_embedding_model():
    global _model
    if _model is None:
        model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        start = time.time()
        _model = SentenceTransformer(model_name)
        print(_model.device)
        print("Loaded in", time.time() - start, "seconds")
    return _model

def embedding_dim():
    return get_embedding_model().get_sentence_embedding_dimension()

def get_embedding(text: str):
    model = get_embedding_model()
    return model.encode(text).tolist()