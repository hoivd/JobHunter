# backend.py
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from concurrent.futures import ThreadPoolExecutor
import subprocess
import os

# IMPORT AGENT CỦA BẠN -------------------------------------------------
# đảm bảo python có thể import package 'agent' (chạy uvicorn từ thư mục gốc hoặc set PYTHONPATH)
from agent.conversation.agent import ConversationalAgent
# ---------------------------------------------------------------------
from fastapi import FastAPI, WebSocket
import uvicorn
from optimize_cv.find_more_info.app import generate_cv

app = FastAPI(title="ConversationalAgent API")


# CORS: cho phép frontend (dev) gọi API (thay đổi allow_origins trong production)
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


# Khởi tạo agent **một lần** khi backend start
agent = ConversationalAgent()
# ThreadPool để chạy các tác vụ blocking (ví dụ agent.chat) ngoài event loop
executor = ThreadPoolExecutor(max_workers=2)


# Model dữ liệu request
class Query(BaseModel):
    text: str


# Route test root (tránh 404 khi mở /)
@app.get("/")
def read_root():
    return {"message": "Backend chạy OK. Gọi POST /chat hoặc connect ws://<host>/ws"}


# REST endpoint: POST /chat
@app.post("/chat")
async def chat(query: Query):
    """Nhận JSON {'text': '...'} và trả {'response': '...'}"""
    loop = asyncio.get_running_loop()
    try:
        # Chạy agent.chat trong thread pool để tránh block event loop
        response = await loop.run_in_executor(executor, agent.chat, query.text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat_query")
async def chat(query: Query):
    """Nhận JSON {'text': '...'} và trả {'response': '...'}"""
    loop = asyncio.get_running_loop()
    try:
        # Chạy agent.chat trong thread pool để tránh block event loop
        response = await loop.run_in_executor(executor, agent.chat, query.text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# WebSocket endpoint: /ws

        
@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_running_loop()
    
    index_file = "retrieval/jobs_index.faiss"
    pkl_file   = "retrieval/id2title.pkl"

    # nếu 2 file đã tồn tại thì bỏ qua build
    if os.path.exists(index_file) and os.path.exists(pkl_file):
        print("✅ Index và PKL đã tồn tại, không cần build lại.")
        return

    def run_index():
        print("🔨 Chạy build_index để tạo FAISS và PKL...")
        subprocess.run(
            ["python", "-m", "retrieval.build_index"],
            check=True
        )

    # chạy trong thread pool để không block event loop
    await loop.run_in_executor(None, run_index)





@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Nhận dữ liệu từ client
            await websocket.send_text("Nhập cv và jd")

            data = await websocket.receive_json()
            cv_info = data.get("cv_info", "")
            jd_info = data.get("jd_info", "")

            # Gọi hàm generate_cv
            tailored_cv = await generate_cv(cv_info, jd_info, websocket)

            # Gửi kết quả trả về
            await websocket.send_json({"tailored_cv": tailored_cv})

    except Exception as e:
        print(e)
        await websocket.close()
        
        
        
    