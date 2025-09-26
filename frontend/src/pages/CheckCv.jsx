import React, { useState } from "react";
import GraphView from "../components/Graph/GraphView";
import Chatbot from "../components/Chatbot/Chatbot";
import ReviewCv from "../components/ReviewCV/ReviewCv";

const CheckCv = () => {
  const [isPreviewCv, setIsPreviewCv] = useState(true);
  return (
    <div
      className={`h-screen w-full ${
        isPreviewCv ? "grid grid-cols-[65%_35%]" : "flex-1"
      }`}
    >
      <div className="h-full w-full relative">
        <GraphView />
      </div>
      <div
        className={`absolute w-[28%] h-[60%] ${
          isPreviewCv ? "bottom-2 left-125" : "bottom-2 right-5"
        }`}
      >
        <Chatbot />
      </div>
      {isPreviewCv && (
        <div className="h-screen">
          <ReviewCv setIsPreviewCv={setIsPreviewCv} />
        </div>
      )}
    </div>
  );
};

export default CheckCv;
