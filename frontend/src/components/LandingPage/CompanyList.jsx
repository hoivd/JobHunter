const CompanyList = ({ logo }) => {
  return (
    <div className="w-26 h-26 bg-white/20 rounded-full flex justify-center items-center">
      <div className="w-24 h-24 rounded-full bg-white border border-white/20 flex justify-center items-center p-4 hover:scale-105 hover:brightness-110 transition-all duration-200">
        <img src={logo} alt="Google" className="w-18 " />
      </div>
    </div>
  );
};

export default CompanyList;
