import sys, time, threading, itertools, json
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
import asyncio
from langchain.prompts import ChatPromptTemplate
import sys

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


async def async_extract_requirements(jd: str):
    return extract_requirements(jd)

async def async_extract_cv_info(cv: str):
    return extract_cv_info(cv)

async def parallel_extract(jd_text: str, cv_text: str):
    jd_task = asyncio.create_task(async_extract_requirements(jd_text))
    cv_task = asyncio.create_task(async_extract_cv_info(cv_text))
    jd_requirements, full_cv_info = await asyncio.gather(jd_task, cv_task)
    return jd_requirements, full_cv_info

def loading_animation(stop_event):
    for c in itertools.cycle([".", "..", "...", ""]):
        if stop_event.is_set():
            break
        sys.stdout.write("\r   Chatbot đang suy nghĩ" + c + "   ")
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write("\r" + " " * 50 + "\r")  # clear line


def typewriter_effect(text, delay=0.03):
    for word in text.split():
        sys.stdout.write(word + " ")
        sys.stdout.flush()
        time.sleep(delay)
    print("\n")
    
    
def generate_gap_question(jd_req, cv_info):
    prompt = gap_prompt.format_messages(
        jd_requirements=json.dumps(jd_req, ensure_ascii=False),
        cv_info=json.dumps(cv_info, ensure_ascii=False)
    )

    # Start loading animation in background
    stop_event = threading.Event()
    t = threading.Thread(target=loading_animation, args=(stop_event,))
    t.start()

    # Call model (blocking)
    resp = llm.invoke(prompt)
    
    # Stop animation
    stop_event.set()
    t.join()

    # Parse JSON
    try:
        parsed = json.loads(resp.content)
    except:
        parsed = normalize_llm_json(resp.content)

    question = parsed.get("question", "DONE")

    # Print nicely
    if question == "DONE":
        print("   Chatbot: Không có gap quan trọng nào. Tiến hành tối ưu CV.\n")
    else:
        sys.stdout.write("   Chatbot: ")
        sys.stdout.flush()
        typewriter_effect(question, delay=0.04)

    return question


def integrate_extra_info(current_cv_info: dict, user_extra_info: str):
    resp = llm.invoke(integrate_extra_info_prompt.format_messages(
        current_cv_info_json=json.dumps(current_cv_info),
        user_extra_info=user_extra_info
    ))
    return normalize_llm_json(resp.content)

def optimize_cv_final(jd: str, full_cv_info: dict):
    resp = llm.invoke(optimize_cv_prompt.format_messages(jd=jd, full_cv_info=json.dumps(full_cv_info)))
    try:
        parsed = json.loads(resp.content)
        return parsed.get("optimized_cv", resp.content)  # chỉ trả CV string
    except:
        parsed = normalize_llm_json(resp.content)
        return parsed.get("optimized_cv", resp.content)


