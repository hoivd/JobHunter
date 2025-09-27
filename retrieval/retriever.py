# retriever.py
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from config.settings import Settings
import os

HF_HOME = os.path.expanduser("retrieval/.cache/huggingface")
os.makedirs(HF_HOME, exist_ok=True)
os.environ["HF_HOME"] = HF_HOME
os.environ["TRANSFORMERS_CACHE"] = HF_HOME

MODEL_NAME = Settings.MODEL_NAME
INDEX_FILE = Settings.INDEX_FILE
MAPPING_FILE = Settings.MAPPING_FILE


class JobRetriever:
    _cached_models = {}

    @classmethod
    def get_model(cls, model_name):
        if model_name not in cls._cached_models:
            print(f"Loading embedding model: {model_name}")
            cls._cached_models[model_name] = SentenceTransformer(
                model_name, cache_folder=HF_HOME
            )
        else:
            print(f"Using cached model: {model_name}")
        return cls._cached_models[model_name]

    def __init__(self, model_name=MODEL_NAME):
        self.model = self.get_model(model_name)  # gọi classmethod
        self.index = None
        self.id2title = None

    def encode_texts(self, texts, batch_size=32):
        """
        Encode danh sách texts thành embeddings numpy.
        """
        return self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
        )

    def build_index(self, job_titles):
        """
        Encode job titles và build FAISS index.
        """
        print("Encoding job titles...")
        job_embs = self.encode_texts(job_titles)
        faiss.normalize_L2(job_embs)

        print("Building FAISS index...")
        self.index = faiss.IndexFlatIP(job_embs.shape[1])
        self.index.add(job_embs)
        self.id2title = {i: t for i, t in enumerate(job_titles)}
        return self.index, self.id2title

    def save_index(self):
        """
        Lưu index và mapping ra file.
        """
        if self.index is None or self.id2title is None:
            raise ValueError("Index chưa được build.")
        faiss.write_index(self.index, INDEX_FILE)
        with open(MAPPING_FILE, "wb") as f:
            pickle.dump(self.id2title, f)
        print("Index & mapping saved!")

    def load_index(self):
        """
        Load index và mapping từ file.
        """
        self.index = faiss.read_index(INDEX_FILE)
        with open(MAPPING_FILE, "rb") as f:
            self.id2title = pickle.load(f)
        print("Index & mapping loaded!")
        return self.index, self.id2title

    def query_from_skills(self, skills, encode_mode="avg", top_k=5):
        if self.index is None or self.id2title is None:
            raise ValueError("Index chưa được build hoặc load.")

        if encode_mode == "avg":
            skill_embs = self.model.encode(skills, convert_to_numpy=True)
            query_vec = np.mean(skill_embs, axis=0, keepdims=True)
        else:
            text = "Skills required for the job: " + " ; ".join(skills)
            query_vec = self.model.encode([text], convert_to_numpy=True)

        faiss.normalize_L2(query_vec)
        D, I = self.index.search(query_vec, top_k)

        results = []
        for j, idx in enumerate(I[0]):
            if idx == -1:  # skip invalid indices
                continue
            results.append((self.id2title[idx], float(D[0][j])))
        return results


    def query_similar_jobs(self, job_title, top_k=5):
        """
        Query các jobs tương tự một job cụ thể.
        """
        if self.index is None or self.id2title is None:
            raise ValueError("Index chưa được build hoặc load.")

        query_vec = self.model.encode([job_title], convert_to_numpy=True)
        faiss.normalize_L2(query_vec)

        D, I = self.index.search(query_vec, top_k)

        results = []
        for j, idx in enumerate(I[0]):
            if idx == -1:  # bỏ qua những kết quả không hợp lệ
                continue
            results.append((self.id2title[idx], float(D[0][j])))

        return results


    def get_jobs_from_skills(self, skills, encode_mode="avg", top_k=5):
        """
        Trả về danh sách job titles từ skill list (không kèm score).
        """
        results = self.query_from_skills(skills, encode_mode=encode_mode, top_k=top_k)
        return [title for title, _ in results]

    def get_similar_jobs(self, job_title, top_k=5):
        """
        Trả về danh sách job titles tương tự job input (không kèm score).
        """
        results = self.query_similar_jobs(job_title, top_k=top_k)
        return [title for title, _ in results]