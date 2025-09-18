import re
from typing import Optional
import json
from pathlib import Path

def extract_json(text: str) -> Optional[str]:
    pattern = r"```json\s*(\{.*?\})\s*```"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1) if match else None

def q(v):
    """Return a JSON-style quoted string for Cypher values (keep unicode)."""
    if v is None:
        return json.dumps("", ensure_ascii=False)
    return json.dumps(v, ensure_ascii=False)

def cypher_props(d):
    """Convert dict -> Cypher props like: name:"...", city:"...\""""
    parts = []
    for k, v in d.items():
        if v is None:
            v = ""
        parts.append(f'{k}:{json.dumps(v, ensure_ascii=False)}')
    return ", ".join(parts)

def cypher_list_of_strings(items):
    """Return a string representing a Cypher list of quoted strings without trailing comma."""
    if not items:
        return "[]"
    quoted = [json.dumps(item, ensure_ascii=False) for item in items]
    return "[\n    " + ",\n    ".join(quoted) + "\n]"

def cypher_list_of_idents(idents):
    """Return a string representing a Cypher list of identifiers like [loc1, loc2]."""
    if not idents:
        return "[]"
    return "[" + ", ".join(idents) + "]"

def generate_cypher_from_json(data: dict, out_path: str = "output_cypher"):
    """Sinh script Cypher từ JSON đầu vào và lưu ra file."""
    lines = []

    # --- NODE chính ---
    lines.append("// =====================")
    lines.append("// TẠO NODE CHÍNH")
    lines.append("// =====================")

    company = data.get("Company", [{}])[0]
    company_props = cypher_props({
        "name": company.get("name", ""),
        "industry": company.get("industry", ""),
        "size": company.get("size", ""),
        "country": company.get("country", "")
    })
    lines.append(f"MERGE (c:Company {{{company_props}}})")
    lines.append('CREATE (jd:JD {name:"JD"})')

    job_title = data.get("JobTitle", [{}])[0]
    jt_name = job_title.get("name", "Job Title")
    lines.append(f'MERGE (j:JOB_TITLE {{name:{json.dumps(jt_name, ensure_ascii=False)}}})')

    lines.append('MERGE (s:SKILL_INCLUDE {name:"SKILL"})')
    lines.append('MERGE (n:BENEFIT_INCLUDE {name:"BENEFIT"})')
    lines.append('MERGE (d:DEGREE_INCLUDE {name:"DEGREE"})')
    lines.append('MERGE (l:LOCATION_INCLUDE {name:"LOCATION"})')
    lines.append('MERGE (t:TASK_INCLUDE {name:"TASK"})')
    lines.append("")

    # --- Skills ---
    skills = data.get("Skill", [])
    if skills:
        lines.append("// =====================")
        lines.append("// TẠO NODE SKILLS")
        lines.append("// =====================")
        skills_list_text = cypher_list_of_strings(skills)
        lines.append("FOREACH (skillName IN " + skills_list_text + " |")
        lines.append("    MERGE (sNode:Skill {name: skillName})")
        lines.append("    MERGE (sNode)-[:REQUIRES_SKILL]->(s)")
        lines.append("    MERGE (s)-[:SKILL_FOR]->(sNode)")
        lines.append(")")
        lines.append("")

    # --- Locations ---
    locations = data.get("Location", [])
    loc_idents = []
    if locations:
        lines.append("// =====================")
        lines.append("// TẠO NODE LOCATION")
        lines.append("// =====================")
        for idx, loc in enumerate(locations, start=1):
            props = cypher_props({
                "city": loc.get("city") or "",
                "district": loc.get("district") or "",
                "address": loc.get("address") or ""
            })
            lines.append(f"MERGE (loc{idx}:Location {{{props}}})")
            loc_idents.append(f"loc{idx}")
        nodes_list = cypher_list_of_idents(loc_idents)
        lines.append("FOREACH (loc IN " + nodes_list + " |")
        lines.append("    MERGE (l)-[:AVAILABLE_AT]->(loc)")
        lines.append("    MERGE (loc)-[:LOCATION_OF]->(l)")
        lines.append(")")
        lines.append("")

    # --- Benefits ---
    benefits = data.get("Benefit", [])
    if benefits:
        lines.append("// =====================")
        lines.append("// TẠO NODE BENEFITS")
        lines.append("// =====================")
        benefits_list_text = cypher_list_of_strings(benefits)
        lines.append("FOREACH (benefitName IN " + benefits_list_text + " |")
        lines.append("    MERGE (b:Benefit {name: benefitName})")
        lines.append("    MERGE (n)-[:OFFERS_BENEFIT]->(b)")
        lines.append("    MERGE (b)-[:BENEFIT_OF]->(n)")
        lines.append(")")
        lines.append("")

    # --- Degrees ---
    degrees = data.get("Degree", [])
    if degrees:
        lines.append("// =====================")
        lines.append("// TẠO NODE DEGREE")
        lines.append("// =====================")
        degrees_list_text = cypher_list_of_strings(degrees)
        lines.append("FOREACH (degreeName IN " + degrees_list_text + " |")
        lines.append("    MERGE (deg:Degree {name: degreeName})")
        lines.append("    MERGE (d)-[:REQUIRES_DEGREE]->(deg)")
        lines.append("    MERGE (deg)-[:DEGREE_OF]->(d)")
        lines.append(")")
        lines.append("")

    # --- Tasks ---
    tasks = data.get("Task", [])
    if tasks:
        lines.append("// =====================")
        lines.append("// TẠO NODE TASK")
        lines.append("// =====================")
        tasks_list_text = cypher_list_of_strings(tasks)
        lines.append("FOREACH (taskName IN " + tasks_list_text + " |")
        lines.append("    MERGE (task:Task {name: taskName})")
        lines.append("    MERGE (t)-[:INCLUDES_RESPONSIBILITY]->(task)")
        lines.append("    MERGE (task)-[:RESPONSIBILITY_OF]->(t)")
        lines.append(")")
        lines.append("")

    # --- Relations giữa node chính ---
    lines.append("// =====================")
    lines.append("// TẠO QUAN HỆ GIỮA CÁC NODE CHÍNH")
    lines.append("// =====================")
    relations = [
        ("c", "HAS_JD", "jd"),
        ("jd", "BELONGS_TO_COMPANY", "c"),
        ("jd", "HAS_JOB_TITLE", "j"),
        ("j", "JOB_TITLE_OF", "jd"),
        ("jd", "INCLUDES_SKILL", "s"),
        ("s", "SKILL_OF", "jd"),
        ("jd", "OFFERS_BENEFIT", "n"),
        ("n", "BENEFIT_OF", "jd"),
        ("jd", "HAS_REQUIREMENT", "d"),
        ("d", "REQUIREMENT_OF", "jd"),
        ("c", "LOCATED_AT", "l"),
        ("l", "LOCATION_OF", "c"),
        ("jd", "HAS_TASK", "t"),
        ("t", "TASK_OF", "jd")
    ]
    for a, r, b in relations:
        lines.append(f"MERGE ({a})-[:{r}]->({b})")

    lines.append("")
    lines.append("// =====================")
    lines.append("// HIỂN THỊ KẾT QUẢ")
    lines.append("// =====================")
    lines.append("WITH *")
    lines.append("MATCH (x)-[y]->(z)")
    lines.append("RETURN x, y, z")

    # --- ghi file ---
    out_path = Path(out_path)
    out_path.write_text("\n".join(lines), encoding="utf-8")

    return "\n".join(lines) 

