from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def load_model(model_name):
    return SentenceTransformer(model_name)

def build_faiss_index(embeddings):
    """
    Xây FAISS Index với cosine similarity (Inner Product sau normalize).
    """
    dim = embeddings.shape[1]
    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index

def encode_texts(model, texts, batch_size=32):
    return model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True
    )