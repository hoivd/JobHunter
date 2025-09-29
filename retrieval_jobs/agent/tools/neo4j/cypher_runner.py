from cypher.cypher_manager import Neo4jDriver
from cypher.query_runner import Neo4jQueryRunner
class CypherRunner:
    def __init__(self):
        self.driver = Neo4jDriver()
        self.runner = Neo4jQueryRunner(self.driver)
        
    def run(self, query: str) -> str:
        results = self.runner.run(query)
        return str(results)