from .cypher_generator import CypherGenerator
from .cypher_runner import CypherRunner

class Neo4jTool:
    def __init__(self):
        self.generator = CypherGenerator()
        self.runner = CypherRunner()
    
    def generate_cypher(self, prompt: str) -> str:
        return self.generator.generate(prompt)

    def run_cypher(self, query: str) -> str:
        return self.runner.run(query)