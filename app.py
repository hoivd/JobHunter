import json
from cypher.generate_code.json2cypher import Json2Cypher
from cypher.cypher_manager import Neo4jDriver
from cypher.generate_code.delete_db import Neo4jCleaner

def main():
    with open("data/data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    converter = Json2Cypher(data)
    converter.save("data/job.cypher")
    with Neo4jDriver() as db:
        q_clean = Neo4jCleaner.delete_all_nodes_and_relationships()
        q_create = converter.to_cypher()
        res = db.run_query(q_clean)
        print(res)
        res = db.run_query(q_create)
        print(res)

def test_neo4j():
    with Neo4jDriver() as db:
        q = "RETURN 'Hello Neo4j' AS msg"
        res = db.run_query(q)
        print(res)

if __name__ == '__main__':
    main()
