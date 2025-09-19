# main.py
from retrieval import query_jobs_from_skills, load_index_and_mapping
from utils import load_model
from config import MODEL_NAME

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
