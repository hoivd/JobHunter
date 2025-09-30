// context/SavedJobsContext.jsx
import { createContext, useContext, useState, useEffect } from "react";

const SavedJobsContext = createContext();

const SavedJobsProvider = ({ children }) => {
  const [savedJobs, setSavedJobs] = useState([]);

  // Khởi tạo từ localStorage
  useEffect(() => {
    const stored = localStorage.getItem("savedJobs");
    if (stored) setSavedJobs(JSON.parse(stored));
  }, []);

  useEffect(() => {
    localStorage.setItem("savedJobs", JSON.stringify(savedJobs));
  }, [savedJobs]);

  const toggleSaveJob = (job) => {
    setSavedJobs((prev) =>
      prev.some((j) => j.id === job.id)
        ? prev.filter((j) => j.id !== job.id)
        : [...prev, job]
    );
  };

  return (
    <SavedJobsContext.Provider value={{ savedJobs, toggleSaveJob }}>
      {children}
    </SavedJobsContext.Provider>
  );
};

// Export đúng chuẩn
export { SavedJobsProvider, SavedJobsContext };

// eslint-disable-next-line react-refresh/only-export-components
export const useSavedJobs = () => useContext(SavedJobsContext);
