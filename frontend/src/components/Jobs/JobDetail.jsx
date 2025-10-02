const JobDetail = ({ job }) => {
  const img = job.Company_Image
    ? `https://drive.google.com/thumbnail?id=${job.Company_Image}`
    : null;
  return (
    <div className="w-full h-full flex flex-col overflow-y-auto no-scrollbar">
      <div className="flex space-x-8 mb-6">
        <div className="shadow-md h-34 rounded-2xl flex items-center justify-center px-4 mr-10">
          <img src={img} alt={job.Company_Name} className="h-20" />
        </div>
        <div className="space-y-2">
          <h1>{job.Company_Name}</h1>
          <h1 className="font-semibold text-lg text-[#192d3c]">
            {job.job_title}
          </h1>
          <div className="flex flex-col  space-y-2">
            <div className="flex space-x-2 items-center px-4 py-1 bg-[#f3fdfe] rounded-2xl w-fit">
            <h1 className="text-[14px]">{job.Company_Country}</h1>
          </div>
          <div className="flex space-x-2 items-center px-4 py-1 bg-[#f3fdfe] rounded-2xl w-fit">
            <h1 className="text-[14px]">{job.Company_Industry}</h1>
          </div>
          </div>
        </div>
      </div>
      <div className="space-y-2">
        
        <div>
          <h1 className="font-semibold">Responsive:</h1>
          {job.Tasks.map((desc, index) => (
            <p key={index} className="text-[14px]">
              • {desc}
            </p>
          ))}
        </div>
        <div>
          <h1 className="font-semibold">Benefits:</h1>
          {job.Benefits.map((desc, index) => (
            <p className="text-[14px]" key={index}>
              • {desc}
            </p>
          ))}
        </div>
        <div className="flex space-x-2 items-center">
          <h1 className="font-semibold">Working hours:</h1>
          <h1 className="text-[14px]">9 a.m - 18 p.m</h1>
        </div>
        <div className="flex space-x-2 items-center">
          <h1 className="font-semibold">Employee:</h1>
          <h1 className="text-[14px]">{job.Company_Size}</h1>
        </div>
      </div>
    </div>
  );
};

export default JobDetail;
