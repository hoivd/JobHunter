import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LiveLatex from "./pages/LiveLatex";

ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<LiveLatex />} />
    </Routes>
  </BrowserRouter>
);
