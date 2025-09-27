import JobCard from "../components/Jobs/JobCard";
import { useSavedJobs } from "../context/SavedJobsContext";

const SavedJob = () => {
  const { savedJobs } = useSavedJobs();

  return (
    <div className="bg-[#f3fdfe] h-screen rounded-l-4xl p-8 flex flex-col items-start justify-start">
      <h1 className="text-3xl font-bold mb-4 text-[#19335a] pl-4">Saved Job</h1>
      <div className="transition-all duration-300 overflow-y-auto no-scrollbar grid grid-cols-3 gap-4 py-2">
        {savedJobs.length === 0 ? (
          <p className="text-gray-600 text-center pl-4">No saved jobs yet.</p>
        ) : (
          savedJobs.map((job) => <JobCard key={job.id} job={job} />)
        )}
      </div>
    </div>
  );
};

export default SavedJob;
