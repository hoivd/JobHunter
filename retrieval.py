import faiss
import pickle
import numpy as np
from config import MODEL_NAME, INDEX_FILE, MAPPING_FILE
from utils import load_model

def query_jobs_from_skills(model, index, id2title, skills, encode_mode="avg", top_k=5):
    """
    skills: list[str]
    encode_mode: "avg" hoặc "concat"
    """
    if encode_mode == "avg":
        skill_embs = model.encode(skills, convert_to_numpy=True)
        query_vec = np.mean(skill_embs, axis=0, keepdims=True)
    else:
        text = " ; ".join(skills)
        query_vec = model.encode([text], convert_to_numpy=True)

    faiss.normalize_L2(query_vec)
    D, I = index.search(query_vec, top_k)

    return [(id2title[idx], float(D[0][j])) for j, idx in enumerate(I[0])]

def load_index_and_mapping():
    index = faiss.read_index(INDEX_FILE)
    with open(MAPPING_FILE, "rb") as f:
        id2title = pickle.load(f)
    return index, id2title

if __name__ == "__main__":
    model = load_model(MODEL_NAME)
    index, id2title = load_index_and_mapping()

    skills = [
        "C Programming",
        "Embedded Systems",
        "Microcontrollers",
        "IoT Protocols",
        "Arduino",
        "Raspberry Pi",
        "MQTT",
        "Wireless Communication",
        "Sensor Integration",
        "Edge Computing"
    ]

    print("\nQuerying for skills:", skills)
    results = query_jobs_from_skills(model, index, id2title, skills)

    print("\nTop job matches:")
    for title, score in results:
        print(f"{title:30s} | score={score:.4f}")
