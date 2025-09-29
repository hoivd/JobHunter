from .retriever import JobRetriever
from cypher.cypher_manager import Neo4jDriver
if __name__ == "__main__":
    
    with Neo4jDriver() as db:
        res = db.run_query("MATCH (jt:JobTitle) RETURN jt.name AS JobTitle")
        job_titles = [r['JobTitle'] for r in res]
        print(job_titles)


    retriever = JobRetriever()
    retriever.build_index(job_titles)
    retriever.save_index()