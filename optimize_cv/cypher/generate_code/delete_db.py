class Neo4jCleaner:
    @staticmethod
    def delete_all_nodes_and_relationships() -> str:
        """
        Trả về query Cypher xóa toàn bộ node và relationship trong DB hiện tại.
        """
        return "MATCH (n) DETACH DELETE n"