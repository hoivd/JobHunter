import { useState, useEffect, useRef } from "react";
import { companyLogos } from "../constants/images";
import { search } from "../constants/icons";
import CompanyList from "../components/LandingPage/CompanyList";
import { useNavigate } from "react-router-dom";
import { WSClient } from "../wsClient";

const LandingPage = () => {
  const navigate = useNavigate();
  const [inputText, setInputText] = useState("");
  const [messages, setMessages] = useState([]);
  const wsRef = useRef(null);

  useEffect(() => {
    wsRef.current = new WSClient("ws://localhost:8000/ws");

    wsRef.current.onMessage((msg) => {
      setMessages((prev) => [...prev, { from: "agent", text: msg }]);
    });

    return () => wsRef.current.close();
  }, []);

  const sendMessage = () => {
    const text = inputText.trim();
    if (!text) return;

    setMessages((prev) => [...prev, { from: "user", text }]);
    wsRef.current.send(text);
    setInputText("");
  };

  return (
    <div
      style={{
        background:
          "linear-gradient(178deg,rgba(25, 51, 90, 1) 10%, rgba(165, 184, 232, 1) 92%)",
      }}
      className="w-full h-screen"
    >
      {/* Header */}
      <div className="px-20 py-8 w-full h-[15%] flex justify-between items-center">
        <img src={companyLogos.jh} alt="Job hunter" className="w-45" />
        <div className="flex quick justify-center items-center space-x-6">
          <button
            onClick={() => navigate("/signin")}
            className="cursor-pointer px-8 py-2 rounded-xl text-white font-semibold"
          >
            <h1>Sign in</h1>
          </button>
          <button
            onClick={() => navigate("/signup")}
            className="cursor-pointer px-8 py-3 rounded-xl text-[#19335A] font-semibold bg-[#A5B8E8] hover:brightness-105 hover:scale-105 transition-all duration-200"
          >
            <h1>Sign up</h1>
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="w-full h-[85%] grid grid-cols-[15%_50%_15%] gap-20 justify-center p-12">
        {/* Left Column */}
        <div className="flex flex-col space-y-10 w-full">
          <div className="flex justify-end">
            <CompanyList logo={companyLogos.apple} />
          </div>
          <div className="flex justify-center">
            <CompanyList logo={companyLogos.google} />
          </div>
          <div className="flex justify-end">
            <CompanyList logo={companyLogos.ms} />
          </div>
        </div>

        {/* Center Column (Chat + Banner) */}
        <div className="flex flex-col items-center space-y-6">
          <h1 className="text-4xl font-bold text-white mb-4">
            Find Your <span className="text-green-500">Perfect Job</span> with AI
          </h1>
          <h1 className="text-2xl font-semibold text-white">
            Optimize Your <span className="text-green-500">CV</span> for Every Opportunity
          </h1>
          <p className="text-gray-100 text-center text-lg max-w-xl mx-auto">
            Discover tailored job matches and smart CV recommendations <br />
            powered by AI — helping you land the right role faster and smarter.
          </p>

          {/* Chat Box */}
          <div className="w-[85%] flex flex-col mt-8">
            <div className="flex border rounded-4xl bg-white shadow-[0_0_9px_0px_rgba(0,0,0,0.25)] p-2 space-x-2">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Talk to AI..."
                className="flex-1 outline-none border-none px-4 py-2 rounded-4xl"
                onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              />
              <button
                onClick={sendMessage}
                className="px-4 py-2 rounded-4xl bg-[#192d3c] text-white font-medium"
              >
                Send
              </button>
            </div>

            {/* Messages */}
            <div className="mt-4 max-h-64 overflow-y-auto bg-gray-200 p-4 rounded-lg">
              {messages.map((m, i) => (
                <div
                  key={i}
                  className={`mb-2 ${m.from === "user" ? "text-right" : "text-left"}`}
                >
                  <span
                    className={`inline-block px-3 py-1 rounded-lg ${
                      m.from === "user" ? "bg-blue-400 text-white" : "bg-green-400 text-white"
                    }`}
                  >
                    {m.text}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="flex flex-col space-y-10 w-full">
          <div className="flex justify-start">
            <CompanyList logo={companyLogos.tesla} />
          </div>
          <div className="flex justify-center">
            <CompanyList logo={companyLogos.oracle} />
          </div>
          <div className="flex justify-start">
            <CompanyList logo={companyLogos.ibm} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
