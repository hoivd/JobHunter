import { companyLogos } from "../constants/images";
import { search } from "../constants/icons";
import CompanyList from "../components/LandingPage/CompanyList";
import { useNavigate } from "react-router-dom";
import { useContext } from "react";
import LanguageContext from "../context/LanguageContext";

const LandingPage = () => {
  const navigate = useNavigate();
  const { lang, toggleLanguage } = useContext(LanguageContext);

  // Text hiển thị theo ngôn ngữ
  const texts = {
    en: {
      title1: "Find Your Perfect Job with AI",
      title2: "Optimize Your CV for Every Opportunity",
      desc: "Discover tailored job matches and smart CV recommendations powered by AI — helping you land the right role faster and smarter.",
      searchPlaceholder: "Search your dream job for your future life",
      signIn: "Sign in",
      signUp: "Sign up",
    },
    vi: {
      title1: "Tìm Công Việc Hoàn Hảo Với AI",
      title2: "Tối Ưu CV Cho Mọi Cơ Hội",
      desc: "Khám phá công việc phù hợp và gợi ý CV thông minh bằng AI — giúp bạn tìm đúng việc nhanh hơn và thông minh hơn.",
      searchPlaceholder: "Tìm công việc mơ ước cho tương lai của bạn",
      signIn: "Đăng nhập",
      signUp: "Đăng ký",
    },
  };

  return (
    <div
      style={{
        background:
          "linear-gradient(178deg,rgba(25, 51, 90, 1) 10%, rgba(165, 184, 232, 1) 92%)",
      }}
      className="w-full h-screen"
    >
      <div className="px-20 pl-8 pr-4 w-full h-[15%] flex justify-between items-center">
        <img src={companyLogos.jh} alt="Job hunter" className="w-45" />
        <div className="flex quick justify-center items-center space-x-6">
          <button
            onClick={() => navigate("/signin")}
            className="cursor-pointer px-8 py-2 rounded-xl text-white font-semibold "
          >
            <h1>{texts[lang].signIn}</h1>
          </button>
          <button
            onClick={() => navigate("/signup")}
            className="cursor-pointer px-8 py-3 rounded-xl text-[#19335A] font-semibold bg-[#A5B8E8] hover:brightness-105 hover:scale-105 transition-all duration-200"
          >
            <h1>{texts[lang].signUp}</h1>
          </button>

          <div className="w-[120px] p-1 h-[38px] ml-8 bg-[#ddd] grid grid-cols-[48%_48%] space-x-2 rounded-4xl">
            <button
              className={`w-full rounded-4xl hover:cursor-pointer hover:brightness-105 ${
                lang === "vi" ? "bg-[#19335A] text-white" : ""
              }`}
              onClick={() => lang !== "vi" && toggleLanguage()}
            >
              <p className="text-center">Vi</p>
            </button>
            <button
              className={`rounded-4xl hover:brightness-105 hover:cursor-pointer ${
                lang === "en" ? "bg-[#19335A] text-white " : ""
              }`}
              onClick={() => lang !== "en" && toggleLanguage()}
            >
              <p className="text-center">En</p>
            </button>
          </div>
        </div>
      </div>

      <div className="w-full h-[85%] grid grid-cols-[15%_50%_15%] gap-20 justify-center p-12">
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

        <div className="flex flex-col items-center space-y-6">
          <h1 className="text-4xl font-bold text-white mb-4">
            {texts[lang].title1.split("Perfect Job").map((part, idx) =>
              idx === 1 ? (
                <span key={idx} className="text-green-500">
                  Perfect Job
                </span>
              ) : (
                part
              )
            )}
          </h1>
          <h1 className="text-2xl font-semibold text-white">
            {texts[lang].title2}
          </h1>
          <p className="text-gray-100 text-center text-lg max-w-xl mx-auto">
            {texts[lang].desc}
          </p>

          <form className="w-[85%] rounded-4xl flex items-center justify-between pl-4 space-x-4 bg-white shadow-[0_0_9px_0px_rgba(0,0,0,0.25)] mt-8">
            <img src={search} alt="Search icon" className="w-6 h-6" />
            <input
              type="text"
              placeholder={texts[lang].searchPlaceholder}
              className="w-full py-2 outline-none border-none"
              onKeyDown={(e) => {
                if (e.key === "Enter") e.preventDefault();
              }}
            />
            <button
              type="submit"
              className="py-3 px-4 rounded-r-4xl cursor-pointer bg-[#192d3c]"
            >
              <p className="text-white font-medium">Search</p>
            </button>
          </form>
        </div>

        {/* Right company logos */}
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
