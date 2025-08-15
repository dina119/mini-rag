import os
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from qdrant_client.http.models import PointStruct
from Services.embeddings import embedding_dim
from typing import List


def get_qdrant_client():
    host = os.getenv("QDRANT_HOST", "localhost")
    port = int(os.getenv("QDRANT_PORT", "6333"))
    return QdrantClient(host=host, port=port)

COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "rag_chunks")

def ensure_collection():
    client = get_qdrant_client()
    try:
        client.get_collection(collection_name=COLLECTION_NAME)
    except Exception:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=rest.VectorParams(size=embedding_dim(), distance=rest.Distance.COSINE)
        )
    return COLLECTION_NAME

def upsert_points(points: List[PointStruct]):
    client = get_qdrant_client()
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    
def search(collection_name, query_vector, top_k=5, filter=None):
    client = get_qdrant_client()
    return client.search(collection_name=collection_name, query_vector=query_vector, limit=top_k, query_filter=filter)
    


