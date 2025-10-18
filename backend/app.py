from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from optimize_cv.find_more_info.app import generate_cv

app = FastAPI()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # domain của frontend
    allow_credentials=True,
    allow_methods=["*"],   # có thể giới hạn GET, POST nếu muốn
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Nhắn cho client nhập dữ liệu
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
