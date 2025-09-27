import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import Dashboard from "./pages/Dashboard";
import Signin from "./pages/authentication/Signin";
import Signup from "./pages/authentication/Signup";
import CheckCv from "./pages/CheckCv";
import LanguageProvider from "./context/LanguadeProvider";
import Loading from "./components/Loading";
import { SavedJobsProvider } from "./context/SavedJobsContext";
import SavedJob from "./pages/SavedJob";

const App = () => {
  return (
    <LanguageProvider>
      <SavedJobsProvider>
        <Router>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/signin" element={<Signin />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/checkcv" element={<CheckCv />} />
            <Route path="/loading" element={<Loading />} />
          </Routes>
        </Router>
      </SavedJobsProvider>
    </LanguageProvider>
  );
};

export default App;
