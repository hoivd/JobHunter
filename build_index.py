import pickle
import faiss
from config import MODEL_NAME, INDEX_FILE, MAPPING_FILE
from utils import load_model, encode_texts, build_faiss_index

def build_index(job_titles):
    # 1) Load model
    print("Loading JobBERT-v2...")
    model = load_model(MODEL_NAME)

    # 2) Encode job titles
    print("Encoding job titles...")
    job_embs = encode_texts(model, job_titles)
    print("Embeddings shape:", job_embs.shape)

    # 3) Build FAISS index
    print("Building FAISS index...")
    index = build_faiss_index(job_embs)
    id2title = {i: t for i, t in enumerate(job_titles)}

    # 4) Save index & mapping
    faiss.write_index(index, INDEX_FILE)
    with open(MAPPING_FILE, "wb") as f:
        pickle.dump(id2title, f)
    print("Index & mapping saved!")

if __name__ == "__main__":
    job_titles = [
        "AI Engineer",
        "Machine Learning Engineer",
        "Data Scientist",
        "Software Engineer",
        "DevOps Engineer",
        "Data Engineer",
        "Research Scientist - NLP",
        "IoT Engineer"
    ]
    build_index(job_titles)
