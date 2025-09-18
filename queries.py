from db import driver
import networkx as nx
import matplotlib.pyplot as plt

# -------------------------
# NODE CRUD
# -------------------------
def create_node(label, properties: dict):
    """Tạo một node bất kỳ với label và properties"""
    props_str = ", ".join([f"{k}: ${k}" for k in properties.keys()])
    query = f"CREATE (n:{label} {{ {props_str} }}) RETURN n"
    with driver.session() as session:
        result = session.run(query, **properties)
        node = result.single()["n"]
    print(f"Đã tạo node {label} với properties: {properties}")
    return node


def delete_node(label, property_key, property_value):
    """Xóa node dựa trên label và property xác định"""
    query = f"MATCH (n:{label} {{{property_key}: $value}}) DETACH DELETE n"
    with driver.session() as session:
        session.run(query, value=property_value)
    print(f"Đã xóa node {label} với {property_key}={property_value}")


def get_nodes(label, limit=10):
    """Lấy danh sách node theo label"""
    query = f"MATCH (n:{label}) RETURN n LIMIT {limit}"
    with driver.session() as session:
        result = session.run(query)
        nodes = [record["n"] for record in result]
    return nodes


# -------------------------
# RELATIONSHIP CRUD
# -------------------------
def create_relationship(label1, prop1, value1, 
                        label2, prop2, value2,
                        rel_type, rel_properties=None):
    """Tạo một relationship giữa 2 node bất kỳ"""
    rel_properties = rel_properties or {}
    props_str = ", ".join([f"{k}: ${k}" for k in rel_properties.keys()])
    props_str = f"{{{props_str}}}" if props_str else ""
    
    query = f"""
    MATCH (a:{label1} {{{prop1}: $value1}})
    MATCH (b:{label2} {{{prop2}: $value2}})
    CREATE (a)-[r:{rel_type} {props_str}]->(b)
    RETURN r
    """
    
    with driver.session() as session:
        result = session.run(query, value1=value1, value2=value2, **rel_properties)
        rel = result.single()["r"]
    print(f"Đã tạo relationship {rel_type} giữa {label1}:{value1} → {label2}:{value2}")
    return rel


def delete_relationship(label1, prop1, value1, 
                        label2, prop2, value2,
                        rel_type):
    """Xóa relationship giữa 2 node dựa trên label + property"""
    query = f"""
    MATCH (a:{label1} {{{prop1}: $value1}})-[r:{rel_type}]->(b:{label2} {{{prop2}: $value2}})
    DELETE r
    """
    
    with driver.session() as session:
        session.run(query, value1=value1, value2=value2)
    print(f"Đã xóa relationship {rel_type} giữa {label1}:{value1} → {label2}:{value2}")


def get_relationships(limit=10):
    """Lấy danh sách relationship"""
    query = f"MATCH (a)-[r]->(b) RETURN a,r,b LIMIT {limit}"
    with driver.session() as session:
        result = session.run(query)
        rels = [{"start": record["a"], "rel": record["r"], "end": record["b"]} for record in result]
    return rels

# -------------------------
# VISUALIZATION CRUD
# -------------------------
def visualize_graph(limit=50):
    """
    Truy vấn Neo4j và vẽ graph trực tiếp trong Python
    limit: số lượng relationship tối đa lấy về (để không quá tải)
    """
    query = f"""
    MATCH (a)-[r]->(b)
    RETURN a, r, b
    LIMIT {limit}
    """

    with driver.session() as session:
        result = session.run(query)
        edges = []
        nodes = set()
        for record in result:
            # Lấy tên node hoặc fallback sang id nếu không có name
            a = record["a"].get("name", str(record["a"].id))
            b = record["b"].get("name", str(record["b"].id))
            rel = record["r"].type
            edges.append((a, b, rel))
            nodes.add(a)
            nodes.add(b)

    # Tạo graph hướng
    G = nx.DiGraph()
    for a, b, rel in edges:
        G.add_edge(a, b, label=rel)

    # Vẽ graph
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.5, seed=42)  # bố cục tự động
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=10, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(a,b):r for a,b,r in edges}, font_color='red')
    plt.title(f"Visualize Graph (limit={limit})")
    plt.show()
    
# -------------------------
# EXTRACTIONS JD
# -------------------------
def push_cypher_code(cypher_code: str):
    query = cypher_code
    with driver.session() as session:
        result = session.run(query)
    print(f"Đã thực thi Cypher query: {query}")
    return result
