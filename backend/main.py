# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Load biến môi trường
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")         # ví dụ: "neo4j+s://<your-database>.databases.neo4j.io"
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

app = FastAPI()

# CORS để frontend fetch được
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Kết nối Neo4j Aura
driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)

@app.get("/api/graph")
@app.get("/api/graph")
def get_graph():
    nodes_dict = {}   # id -> node
    links = []

    with driver.session() as session:
        result = session.run("MATCH (n)-[r]->(m) RETURN n,r,m LIMIT 100")
        for record in result:
            n = record["n"]
            m = record["m"]
            r = record["r"]

            # node labels
            n_label = n.get("name") or (next(iter(n.labels)) if n.labels else "Unknown")
            m_label = m.get("name") or (next(iter(m.labels)) if m.labels else "Unknown")

            # Thêm vào dict node duy nhất
            nodes_dict[str(n.id)] = {"id": str(n.id), "label": n_label}
            nodes_dict[str(m.id)] = {"id": str(m.id), "label": m_label}

            # Thêm link
            links.append({"source": str(n.id), "target": str(m.id), "type": r.type})

    return {"nodes": list(nodes_dict.values()), "links": links}

# Đóng driver khi shutdown server
@app.on_event("shutdown")
def shutdown_driver():
    driver.close()
