# backend.py
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from concurrent.futures import ThreadPoolExecutor


# IMPORT AGENT CỦA BẠN -------------------------------------------------
# đảm bảo python có thể import package 'agent' (chạy uvicorn từ thư mục gốc hoặc set PYTHONPATH)
from agent.conversation.agent import ConversationalAgent
# ---------------------------------------------------------------------


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


# WebSocket endpoint: /ws
@app.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    """Mở kết nối WebSocket. Client gửi text, server trả text. Lặp mãi trong khi kết nối mở."""
    await websocket.accept()
    loop = asyncio.get_running_loop()
    try:
        while True:
            text = await websocket.receive_text() # chờ message từ client
            # xử lý blocking tương tự bằng run_in_executor
            response = await loop.run_in_executor(executor, agent.chat, text)
            await websocket.send_text(response)
    except Exception:
        await websocket.close()