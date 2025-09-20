import { address, salary } from "../../constants/icons";

const JobCard = ({ job, setIsJobComp }) => {
  return (
    <div
      onClick={() => setIsJobComp(job)}
      className="w-full  max-h-[450px] bg-white shadow-md rounded-2xl 
             py-4 px-6 flex flex-col justify-between space-y-2 
             hover:brightness-105 hover:scale-[1.02] 
             duration-300 transform transition-all cursor-pointer"
    >
      <div className="flex space-x-4">
        <img
          src={job.img}
          alt={job.company}
          className="w-20 h-auto object-contain"
        />
        <div>
          <h1 className="font-medium">{job.company}</h1>
          <h1 className="text-lg md:text-xl font-semibold text-[#192d3c]">
            {job.position}
          </h1>
        </div>
      </div>
      <div>
        <h1 className="font-semibold">Benefit:</h1>
        {job.benefits.map((benefit, index) => (
          <div>
            <p key={index} className="text-sm text-gray-600">
              - {benefit}
            </p>
          </div>
        ))}
      </div>
      <div className="flex space-x-8 ">
        <div className="flex items-center space-x-2">
          <img src={address} alt={job.city} className="w-4" />
          <h1 className="text-[15px]">{job.city}</h1>
        </div>
        <div className="flex items-center space-x-2">
          <img src={salary} alt={job.city} className="w-4" />
          <h1 className="text-[15px] font-semibold text-[#192d3c]">
            {job.salary}
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
      </div>
    </div>
  );
};

export default JobCard;
