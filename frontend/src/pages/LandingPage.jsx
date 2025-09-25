import { useState } from "react";
import { companyLogos } from "../constants/images";
import { search } from "../constants/icons";
import CompanyList from "../components/LandingPage/CompanyList";
import { useNavigate } from "react-router-dom";
import { chatWithAgent } from "../api"; // đảm bảo path đúng

const LandingPage = () => {
  const navigate = useNavigate();
  const [inputText, setInputText] = useState("");
  const [responseText, setResponseText] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText) return;

    const response = await chatWithAgent(inputText);
    setResponseText(response); // lưu response để hiển thị
    setInputText(""); // xóa input sau khi gửi
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

        {/* Center Column */}
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

          {/* Form Chat */}
          <form
            onSubmit={handleSubmit}
            className="w-[85%] rounded-4xl flex items-center justify-between pl-4 space-x-4 bg-white shadow-[0_0_9px_0px_rgba(0,0,0,0.25)] mt-8"
          >
            <img src={search} alt="Search icon" className="w-6 h-6" />
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Search your dream job for your future life"
              className="w-full py-2 outline-none border-none"
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
            />
            <button
              type="submit"
              className="py-3 px-4 rounded-r-4xl cursor-pointer bg-[#192d3c]"
            >
              <p className="text-white font-medium">Search</p>
            </button>
          </form>

          {/* Hiển thị kết quả từ backend */}
          {responseText && (
            <div className="mt-4 p-4 bg-gray-200 rounded-lg w-[85%] text-black">
              <b>Agent trả lời:</b> {responseText}
            </div>
          )}
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
