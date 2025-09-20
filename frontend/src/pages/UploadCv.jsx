import React from "react";
import FileUpload from "../components/UploadCV/FileUpload";
import GithubAttached from "../components/UploadCV/GithubAttached";

const UploadCv = () => {
  return (
    <div className="bg-[#f3fdfe] h-screen rounded-l-4xl pl-10 flex items-center justify-center">
      <div className="w-[80%] h-[70%] bg-white shadow-lg rounded-3xl flex flex-col items-center justify-center space-y-8 my-4">
        <div className="grid grid-cols-[48%_1%_48%] w-full justify-between">
          <FileUpload />
          <div>
            <div className="w-[2px] h-full bg-[#eee]"></div>
          </div>
          <GithubAttached />
        </div>
        <button
          style={{
            background: "linear-gradient(to bottom, #19335a, #697a98)",
          }}
          className="max-w-[20%] py-[10px] px-8 text-white rounded-xl hover:brightness-120 cursor-pointer hover:scale-105 duration-300 transform transition-all"
        >
          <p className="font-semibold text-[16px]">Check CV</p>
        </button>
      </div>
    </div>
  );
};

export default UploadCv;
