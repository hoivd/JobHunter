import React, { useEffect, useState } from "react";
import { ai } from "../constants/icons";

const Loading = () => {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((old) => {
        if (old >= 100) {
          clearInterval(interval);
          return 100;
        }
        return old + 2;
      });
    }, 100);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col space-y-4 items-center justify-center w-full h-screen bg-[#d3e7f7]">
      <div className="relative w-[25%] h-10 border-2 border-[#07689f] rounded-xl bg-yellow-50 z-0">
        <div
          className="h-full bg-[#98dbee] transition-all duration-200 rounded-xl"
          style={{ width: `${progress}%` }}
        ></div>
        <span className="absolute inset-0 flex items-center justify-center text-white font-semibold">
          Loading...
        </span>
        <div
          className="absolute -top-3 z-20 transition-all duration-200 flex justify-center items-center"
          style={{
            left: `${progress}%`,
            transform: "translate(-50%, 0)",
          }}
        >
          <div className="w-15 h-15 rounded-full flex items-center justify-center shadow-lg">
            <img src={ai} alt="AI" className="w-full h-full" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Loading;
