import json
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from prompt import (
    extract_cv_prompt,
    extract_jd_prompt,
    optimize_cv_prompt,
    gap_prompt,
    integrate_extra_info_prompt,
)

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY chưa được thiết lập trong .env")

# Khởi tạo model gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    google_api_key=GOOGLE_API_KEY
)

def normalize_llm_json(llm_output: str):
    """Attempt to parse LLM output as JSON, handling potential extraneous text."""
    try:
        first_brace = llm_output.find('{')
        last_brace = llm_output.rfind('}')
        if first_brace != -1 and last_brace != -1:
            json_str = llm_output[first_brace : last_brace + 1]
            return json.loads(json_str)
        else:
            return json.loads(llm_output)
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from LLM output: {llm_output}")
        return {"raw_output": llm_output} # Trả về raw output hoặc dict rỗng để xử lý sau

def extract_requirements(jd: str):
    resp = llm.invoke(extract_jd_prompt.format_messages(jd=jd))
    return normalize_llm_json(resp.content)

def extract_cv_info(cv: str):
    resp = llm.invoke(extract_cv_prompt.format_messages(cv=cv))
    return normalize_llm_json(resp.content)

def generate_gap_question(jd_req, cv_info):
    resp = llm.invoke(gap_prompt.format_messages(jd_requirements=json.dumps(jd_req), cv_info=json.dumps(cv_info)))
    try:
        return json.loads(resp.content)["question"]
    except:
        return normalize_llm_json(resp.content)

def integrate_extra_info(current_cv_info: dict, user_extra_info: str):
    resp = llm.invoke(integrate_extra_info_prompt.format_messages(
        current_cv_info_json=json.dumps(current_cv_info),
        user_extra_info=user_extra_info
    ))
    return normalize_llm_json(resp.content)

def optimize_cv_final(jd: str, full_cv_info: dict):
    resp = llm.invoke(optimize_cv_prompt.format_messages(jd=jd, full_cv_info=json.dumps(full_cv_info)))
    try:
        return json.loads(resp.content)["optimized_cv"]
    except:
        return normalize_llm_json(resp.content)


