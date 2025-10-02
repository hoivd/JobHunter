import { address, salary } from "../../constants/icons";
import { useSavedJobs } from "../../context/SavedJobsContext";
import { save, saved } from "../../constants/icons";

const JobCard = ({ job, setIsJobComp }) => {
  const { savedJobs, toggleSaveJob } = useSavedJobs();
  const isSaved = savedJobs.some(
    (j) => j.Company_Name === job.Company_Name && j.JD_Name === job.JD_Name
  );
  const img = job.Company_Image
    ? `https://drive.google.com/thumbnail?id=${job.Company_Image}`
    : null;

  return (
    <div
      onClick={() => setIsJobComp(job)}
      className="w-full  max-h-[400px] bg-white shadow-md rounded-2xl 
             py-4 px-6 flex flex-col justify-between space-y-2 
             hover:brightness-105 hover:scale-[1.02] 
             duration-300 transform transition-all cursor-pointer relative"
    >
      <div className="flex space-x-4">
  <img
    src={img}
    alt={job.Company_Name}
    className="w-20 h-auto object-contain"
  />
  <div>
          <h1 className="font-medium">{job.Company_Name}</h1>
          <h1 className="text-lg md:text-xl font-semibold text-[#192d3c]">
            {job.job_title}
          </h1>
        </div>
</div>

<div>
        <h1 className="font-semibold">Benefit:</h1>
        {job.Benefits?.slice(0,5).map((benefit, index) => (
          <div>
            <p key={index} className="text-sm text-gray-600">
              - {benefit}
            </p>
          </div>
        ))}
      </div>

<div className="flex space-x-8">
  <div className="flex items-center space-x-2">
    <img src={address} alt={job.Company_Country} className="w-4" />
    <h1 className="text-[15px]">{job.Company_Country}</h1>
  </div>
  <div className="flex items-center space-x-2">
    <img src={salary} alt={job.Company_Name} className="w-4" />
    <h1 className="text-[15px] font-semibold text-[#192d3c]">
      {job.salary || (
        job.Benefits && 
        job.Benefits.find(b => b.toLowerCase().includes("salary")) || 
        "Competitive"
      )}
    </h1>
  </div>
</div>

      <div className="flex justify-center space-x-6 ">
        <button className="text-[12px] py-2 px-8 text-[#19335a] border-[1px] border-[#192d3c] rounded-2xl hover:brightness-120 cursor-pointer hover:scale-95 duration-300 transform transition-all">
          <p className="font-semibold">Check CV</p>
        </button>
        <button className=" text-[12px] py-2 px-8 bg-[#19335a] text-white rounded-2xl hover:brightness-120 cursor-pointer hover:scale-95 duration-300 transform transition-all">
          <p className="font-semibold">Detail JD</p>
        </button>
        <button
          onClick={(e) => {
            e.stopPropagation();
            toggleSaveJob(job);
          }}
          className="w-8 h-8 absolute top-2 right-5 bg-gray-100 flex justify-center items-center rounded-lg hover:cursor-pointer"
        >
          {isSaved ? (
            <img src={saved} alt="Saved" className="w-6 h-6" />
          ) : (
            <img src={save} alt="Save" className="w-6 h-6" />
          )}
        </button>
      </div>
    </div>
  );
};

export default JobCard;
