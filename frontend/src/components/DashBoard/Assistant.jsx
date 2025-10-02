import { useState, useRef } from "react";

const Assistant = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const inputRef = useRef(null);

  const sendMessage = async () => {
    const text = inputRef.current.value.trim();
    if (!text) return;

    const newMessage = { text, sender: "user" };
    setMessages((prev) => [...prev, newMessage]);
    inputRef.current.value = "";

    try {
      const response = await fetch("http://localhost:8000/chat_query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await response.json();
      setMessages((prev) => [...prev, { text: data.response, sender: "bot" }]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [...prev, { text: "Error from assistant.", sender: "bot" }]);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="fixed bottom-6 right-6 flex flex-col items-end z-50">
      {/* Chat Box */}
      {isOpen && (
        <div className="w-80 h-96 bg-white rounded-xl shadow-lg flex flex-col overflow-hidden">
          <div className="bg-[#192d3c] text-white px-4 py-2 flex justify-between items-center">
            <h3 className="font-semibold">Assistant</h3>
            <button onClick={() => setIsOpen(false)} className="text-white font-bold">
              X
            </button>
          </div>
          <div className="flex-1 p-3 overflow-y-auto flex flex-col gap-2">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`p-2 rounded-lg max-w-[80%] ${
                  msg.sender === "user" ? "bg-[#e0f0ff] self-end" : "bg-[#f0f0f0] self-start"
                }`}
              >
                {msg.text}
              </div>
            ))}
          </div>
          <div className="p-2 border-t border-gray-200 flex">
            <input
              ref={inputRef}
              type="text"
              placeholder="Ask me..."
              className="flex-1 border rounded-lg px-3 py-2 outline-none"
              onKeyDown={handleKeyDown}
            />
            <button
              onClick={sendMessage}
              className="ml-2 px-3 py-2 bg-[#192d3c] text-white rounded-lg"
            >
              Send
            </button>
          </div>
        </div>
      )}

      {/* Assistant Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-14 h-14 rounded-full bg-[#19335a] text-white font-bold shadow-lg flex items-center justify-center hover:scale-105 transition-transform"
      >
        🤖
      </button>
    </div>
  );
};

export default Assistant;
