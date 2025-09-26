import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import Dashboard from "./pages/Dashboard";
import Signin from "./pages/authentication/Signin";
import Signup from "./pages/authentication/Signup";
import CheckCv from "./pages/CheckCv";
import LanguageProvider from "./context/LanguadeProvider";

const App = () => {
  return (
    <LanguageProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/signin" element={<Signin />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/checkcv" element={<CheckCv />} />
        </Routes>
      </Router>
    </LanguageProvider>
  );
};

export default App;
