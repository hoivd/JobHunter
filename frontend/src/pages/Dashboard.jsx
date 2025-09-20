import React, { useState } from "react";
import Navbar from "../components/Navbar";
import DashBoardCont from "../components/DashBoard/DashboardCont";
import UploadCv from "./UploadCv";

const Dashboard = () => {
  const [isActive, setIsActive] = useState("Dashboard");
  const button = ["Dashboard", "My Profile", "Saved Job", "Upload CV"];

  return (
    <div
      className="w-full h-screen grid grid-cols-[15%_85%]"
      style={{
        background: "linear-gradient(to right, #19335a, #697a98)",
      }}
    >
      <Navbar isActive={isActive} setIsActive={setIsActive} button={button} />
      {isActive === "Dashboard" && <DashBoardCont />}
      {isActive === "Upload CV" && <UploadCv />}
    </div>
  );
};

export default Dashboard;
