import json
from pathlib import Path

class Json2Cypher:
    def __init__(self, data: dict):
        self.entities = data.get("entity", {})
        self.relationships = data.get("relationship", {})
        self.cypher_nodes = ""
        self.cypher_rels = ""
        self.cypher_script = ""

    def _preprocess_entities(self):
        """
        Tiền xử lý entity để quyết định mode (create/merge).
        - Company, JobTitle => merge
        - Các entity khác   => create
        """
        for entity_name, entity_data in self.entities.items():
            # nếu chưa có mode thì set mặc định theo rule
            if "mode" not in entity_data:
                if entity_name in ["Company", "JobTitle"]:
                    entity_data["mode"] = "merge"
                else:
                    entity_data["mode"] = "create"

            # nếu thiếu isGroup thì mặc định là False
            if "isGroup" not in entity_data:
                entity_data["isGroup"] = False

    def _wrap_call(self, body: str) -> str:
        """Bọc 1 đoạn Cypher thành CALL { ... }"""
        return f"CALL {{\n{body.strip()}\n}}"
    
    def _create_node(self, label: str, props: dict, alias: str = None, return_out: bool = True) -> str:
        """Tạo node mới (CREATE), không merge"""
        alias = alias or label.lower()
        props_str = ", ".join([f'{k}: "{v}"' for k, v in props.items() if v is not None])
        body = f"CREATE ({alias}:{label} {{{props_str}}})"
        if return_out:
            body += f"\nRETURN {alias}"
        return body

    def _merge_node(self, label: str, props: dict, alias: str = None, return_out: bool = True) -> str:
        alias = alias or label.lower()
        props_str = ", ".join([f'{k}: "{v}"' for k, v in props.items() if v is not None])
        body = f"MERGE ({alias}:{label} {{{props_str}}})"
        if return_out:
            body += f"\nRETURN {alias}"
        return body

    def _merge_list_node(self, label: str, values: list, key: str = "name", return_out: bool = True) -> str:
        def to_cypher_value(v):
            if isinstance(v, dict):
                props = ", ".join([f'{kk}: "{vv}"' for kk, vv in v.items()])
                return "{" + props + "}"

        values_str = ", ".join([to_cypher_value(v) for v in values])
        alias = label.lower()

        body = f"""
            WITH [{values_str}] AS items
            UNWIND items AS val
            MERGE ({alias}:{label} {{
            {", ".join([f"{k}: val.{k}" for k in values[0].keys()])}
            }})
            """

        if return_out:
            body += f"\nRETURN collect({alias}) AS {alias}s_list"
        return body

    def generate_node(self, entity_name: str, entity_data: dict, alias: str = None):
        """Sinh Cypher cho 1 node"""
        print(f"Entity data  {entity_data}")
        if entity_data["mode"] == "create":
            return self._create_node(entity_name, entity_data, alias)
        elif entity_data["mode"] == "merge":
            return self._merge_node(entity_name, entity_data, alias)
        else:
            raise ValueError(f"Unsupported mode: {entity_data['mode']}")
    
    def generate_group_nodes(self, entity_name: str, entity_data: dict, blocks: list):
        """Sinh Cypher cho các node group"""
        # Node group
        group_node = self.generate_node(entity_name, {"name": entity_name, 'mode': entity_data['mode']}, alias=entity_name.lower())
        blocks.append(self._wrap_call(group_node))

        if len(entity_data['items']) > 0:
            # Child nodes
            items = entity_data["items"]
            child_label = entity_name[:-1] if entity_name.endswith("s") else entity_name + "Item"
            block = self._merge_list_node(child_label, items)
            blocks.append(self._wrap_call(block))

    def generate_single_node(self, entity_name: str, entity_data: dict, blocks: list):
        """Sinh Cypher cho các node đơn lẻ"""
        props = {k: v for k, v in entity_data.items() if k != "isGroup"}
        node_block = self.generate_node(entity_name, props, alias=entity_name.lower())
        blocks.append(self._wrap_call(node_block))

    def generate_nodes(self):
        """Sinh Cypher cho các node"""
        blocks = []
        for entity_name, entity_data in self.entities.items():
            if entity_data["isGroup"]:
                self.generate_group_nodes(entity_name, entity_data, blocks)
            else:
                self.generate_single_node(entity_name, entity_data, blocks)

        # Ghép nodes lại
        self.cypher_nodes = "\nWITH *\n".join(blocks)

    def generate_single_relationships(self, rel_blocks: list):
        """Sinh relationships đơn lẻ"""
        for pair, rel_type in self.relationships.items():
            left, right = pair.split("-")
            left_alias = left.lower()
            right_alias = right.lower()

            body = (
            f"WITH {left_alias}, {right_alias}\n"
            f"MERGE ({left_alias})-[:{rel_type}]->({right_alias})"
            )
            rel_blocks.append(self._wrap_call(body))

    def generate_group_relationships(self, rel_blocks: list):
        for entity_name, entity_data in self.entities.items():
            if entity_data.get("isGroup", False):
                if len(entity_data["items"]) == 0:
                    continue
                group_alias = entity_name.lower()
                item_label = entity_name[:-1] if entity_name.endswith("s") else entity_name + "Item"
                item_alias = item_label.lower()

                body = (
                    f"WITH {group_alias}, {group_alias}_list\n"
                    f"UNWIND {group_alias}_list AS {item_alias}\n"
                    f"MERGE ({group_alias})-[:CONTAINS]->({item_alias})\n"
                    f"MERGE ({item_alias})-[:BELONGS_TO]->({group_alias})"
                )
                rel_blocks.append(self._wrap_call(body))

    def generate_relationships(self):
        """
        Sinh relationships thành 2 bước, mỗi block bọc trong CALL { ... }:
        B1: Quan hệ giữa các entity theo JSON relationships.
        B2: Quan hệ group -> items (xxx_list).
        """
        rel_blocks = []

        # === B1: Sinh relationships từ JSON ===
        self.generate_single_relationships(rel_blocks)


        # === B2: Quan hệ group -> item list ===
        self.generate_group_relationships(rel_blocks)

        # Ghép tất cả lại bằng WITH *
        self.cypher_rels = "\nWITH *\n".join(rel_blocks)

    def to_cypher(self) -> str:
        self._preprocess_entities()
        self.generate_nodes()
        self.generate_relationships()
        self.cypher_script = f"{self.cypher_nodes}\nWITH *\n{self.cypher_rels}\nRETURN *"
        return self.cypher_script

    def save(self, filepath: str):
        script = self.to_cypher()
        Path(filepath).write_text(script, encoding="utf-8")
        print(f"✅ Cypher script saved to {filepath}")

# ===== Ví dụ sử dụng =====
if __name__ == "__main__":
    with open("../data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    converter = Json2Cypher(data)
    converter.save("job.cypher")