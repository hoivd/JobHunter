import { useState, useEffect, useRef } from "react";
import { robot } from "../../constants/icons";

const Chatbot = () => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]); // Lưu tất cả message
  const ws = useRef(null);
  const messagesEndRef = useRef(null); // để scroll tự động

  // Scroll xuống cuối khi có tin nhắn mới
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Khởi tạo WebSocket khi component mount
  useEffect(() => {
    ws.current = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.current.onopen = () => console.log("WebSocket connected");

    ws.current.onmessage = (event) => {
      let botMessage = "";

      // Xử lý dữ liệu server gửi
      try {
        const data = JSON.parse(event.data);
        botMessage = data.message || data.text || event.data; // fallback nếu JSON không có field
      } catch (err) {
        botMessage = event.data; // nếu server gửi string thuần
      }

      // Thêm message chatbot vào state
      setMessages((prev) => [...prev, { text: botMessage, sender: "bot" }]);
    };

    ws.current.onclose = () => console.log("WebSocket disconnected");

    ws.current.onerror = (err) => console.error("WebSocket error:", err);

    return () => ws.current.close();
  }, []);

  const handleSend = () => {
  if (message.trim() === "" || ws.current.readyState !== WebSocket.OPEN) return;

  // Thêm tin nhắn người dùng vào state
  setMessages((prev) => [...prev, { text: message, sender: "user" }]);

  // Gửi trực tiếp chuỗi thuần lên server
  try {
    ws.current.send(message); // gửi "Xin chào" thay vì {"message": "Xin chào"}
  } catch (err) {
    console.error("Failed to send message:", err);
  }

  setMessage(""); // clear input
};


  return (
    <div className="w-full h-full rounded-2xl p-6 flex flex-col justify-center items-center">
      {/* Header */}
      <h1 className="font-black text-2xl text-green-400 mb-4">
        JobHunter <span className="text-black">Chatbot</span>
      </h1>

      {/* Chat messages */}
      <div className="w-full flex-1 overflow-y-auto p-4 flex flex-col space-y-2">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[60%] px-4 py-2 rounded-xl break-words ${
                msg.sender === "user"
                  ? "bg-blue-500 text-white rounded-br-none"
                  : "bg-gray-200 text-black rounded-bl-none"
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="w-full max-w-[90%] mt-4 grid items-center space-x-2 p-1 rounded-xl bg-white/80 grid-cols-[75%_25%]">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Type a message..."
          className="px-4 py-2 focus:outline-none text-gray-800"
        />
        <button
          onClick={handleSend}
          className="px-5 py-2 bg-[#19335a] text-white rounded-xl font-semibold hover:cursor-pointer hover:brightness-105"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;

