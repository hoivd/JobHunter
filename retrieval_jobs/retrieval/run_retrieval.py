# run_retrieval.py
from .retriever import JobRetriever

if __name__ == "__main__":
    retriever = JobRetriever()
    retriever.load_index()

    # --- Example 1: skills → jobs ---
    skills = [
        "Python",
        "R Programming",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "Pandas",
        "NumPy",
        "Data Visualization",
        "Statistics",
        "Big Data Tools",
        "Feature Engineering",
        "Model Deployment",
    ]

    # --- Example 1: skills → jobs ---
    print("\nTop job matches (titles only):")
    jobs_only = retriever.get_jobs_from_skills(skills, encode_mode="string", top_k=5)
    print(jobs_only)  # ['Deep Learning Engineer', 'Machine Learning Engineer', 'Data Scientist', ...]

    # --- Example 2: job → jobs ---
    print("\nTop similar jobs (titles only):")
    similar_only = retriever.get_similar_jobs("AI engineer", top_k=5)
    print(similar_only)  # ['Data Scientist', 'Data Analyst', 'Machine Learning Engineer', ...]

