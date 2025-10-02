import { useRef, useState } from "react";
import search from "../../assets/icons/search.png";
import JobCard from "../Jobs/JobCard";
import JobDetail from "../Jobs/JobDetail";

const DashBoardCont = () => {
  const [isJobComp, setIsJobComp] = useState(null);
  const inputRef = useRef(null);
  const [jobs, setJobs] = useState([]);


const submitHandler = async (e) => {
  e?.preventDefault(); // ngăn form reload trang
  const text = inputRef.current.value;

  try {
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    const data = await response.json();
    console.log("API response:", data);

    // Lấy trực tiếp jd_details từ backend
    setJobs(data.response.jd_details);

  } catch (error) {
    console.error("Error fetching API:", error);
  }
};





  return (
    <div className="bg-[#f3fdfe] rounded-l-4xl pt-6 pl-10  flex flex-col h-screen">
      <form
        onSubmit={submitHandler}
        className="w-[45%] rounded-4xl flex items-center justify-between pl-4 space-x-4 bg-white shadow-[0_0_9px_0px_rgba(0,0,0,0.25)] mb-6"
      >
        <img src={search} alt="Search icon" className="w-6 h-6" />
        <input
        ref={inputRef}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              submitHandler();
            }
          }}
          type="text"
          className="w-full py-2 outline-none border-none"
          placeholder="Your technical skill, position or more"
        />
        <button
          type="submit"
          onClick={submitHandler}
          className="py-3 px-4 rounded-r-4xl cursor-pointer bg-[#192d3c]"
        >
          <p className="text-white font-medium">Search</p>
        </button>
      </form>
      <div className="flex flex-1 h-full space-x-6 overflow-hidden">
        {/* Job List */}
        <div
          className={`transition-all duration-300 overflow-y-auto no-scrollbar grid gap-6 py-2 pl-2 pr-8
      ${
        isJobComp
          ? "flex-[0.6] grid-cols-1 md:grid-cols-2"
          : "flex-1 grid-cols-1 md:grid-cols-2 lg:grid-cols-3"
      }
    `}
        >
          {jobs.map((job, index) => (
            <JobCard key={index} job={job} setIsJobComp={setIsJobComp} />
          ))}
        </div>

        {/* Job Detail */}
        {isJobComp && (
          <div className="flex-[0.4] h-full bg-white shadow-lg rounded-xl py-4 px-6 overflow-y-auto no-scrollbar relative">
            <div className="h-[90%] w-full">
              <JobDetail job={isJobComp} />
            </div>
            <div className="h-[8%] w-full flex justify-between items-center mt-4">
              <button
                onClick={() => {
                  setIsJobComp(null);
                }}
                className="py-2 px-8 border-[1px] border-[#192d3c] rounded-xl hover:bg-[#192d3c] hover:text-white cursor-pointer hover:scale-105 duration-300 transform transition-all"
              >
                <p className="font-semibold text-[14px]">Back</p>
              </button>
              <button
                style={{
                  background: "linear-gradient(to bottom, #19335a, #697a98)",
                }}
                className=" py-[10px] px-8 text-white rounded-xl hover:brightness-120 cursor-pointer hover:scale-105 duration-300 transform transition-all"
              >
                <p className="font-semibold text-[14px]">Check CV</p>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DashBoardCont;
