import { useState } from "react";
import { robot } from "../../constants/icons";

const Chatbot = () => {
  const [message, setMessage] = useState("");

  const handleSend = () => {
    if (message.trim() === "") return;
    console.log("Send:", message);
    setMessage(""); // clear sau khi gửi
  };

  return (
    <div className="w-full h-full rounded-2xl p-12 flex flex-col items-center">
      {/* Header */}
      <h1 className="font-black text-2xl text-green-400">
        JobHunter <span className="text-black">Chatbot</span>
      </h1>

      {/* Nội dung chính */}
      <div className="flex flex-col justify-center items-center flex-1">
        <img src={robot} alt="Can I help you" className="w-18" />
        <h1 className="font-semibold text-black text-lg">Hello, Alan</h1>
        <h1 className="font-normal text-black">How can I help you?</h1>
      </div>

      <div className="w-full max-w-[60%] grid items-center space-x-2 p-1 rounded-xl bg-white/80 grid-cols-[75%_25%]">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Type a message..."
          className=" px-4 py-2 focus:outline-none text-gray-800"
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
