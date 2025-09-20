const JobDetail = ({ job }) => {
  return (
    <div className="w-full h-full flex flex-col overflow-y-auto no-scrollbar">
      <div className="flex space-x-8 justify-center mb-6">
        <div className="shadow-md h-34 rounded-2xl flex items-center justify-center px-4">
          <img src={job.img} alt={job.company} className="h-26" />
        </div>
        <div className="space-y-2">
          <h1>{job.company}</h1>
          <h1 className="font-semibold text-lg text-[#192d3c]">
            {job.position}
          </h1>
          <div className="flex space-x-2 items-center px-4 py-1 bg-[#f3fdfe] rounded-2xl w-fit">
            <h1 className="text-[14px]">{job.city}</h1>
          </div>
          <div className="flex space-x-2 items-center px-4 py-1 bg-[#f3fdfe] rounded-2xl w-fit">
            <h1 className="text-[14px]">{job.working_hours}</h1>
          </div>
        </div>
      </div>
      <div className="space-y-2">
        <div>
          <h1 className="font-semibold ">About Job:</h1>
          {job.job_description.map((desc, index) => (
            <p className="text-[14px]" key={index}>
              • {desc}
            </p>
          ))}
        </div>
        <div>
          <h1 className="font-semibold">Requirement:</h1>
          {job.requirements.map((desc, index) => (
            <p key={index} className="text-[14px]">
              • {desc}
            </p>
          ))}
        </div>
        <div>
          <h1 className="font-semibold">Benefits:</h1>
          {job.benefits.map((desc, index) => (
            <p className="text-[14px]" key={index}>
              • {desc}
            </p>
          ))}
        </div>
        <div className="flex space-x-2 items-center">
          <h1 className="font-semibold">Working hours:</h1>
          <h1 className="text-[14px]">{job.working_hours}</h1>
        </div>
        <div className="flex space-x-2 items-center">
          <h1 className="font-semibold">Location:</h1>
          <h1 className="text-[14px]">{job.location}</h1>
        </div>
        <div className="flex space-x-2 items-center">
          <h1 className="font-semibold">Salary:</h1>
          <h1 className="text-[14px] font-semibold text-[#192d3c]">
            {job.salary}
          </h1>
        </div>
      </div>
    </div>
  );
};

export default JobDetail;
