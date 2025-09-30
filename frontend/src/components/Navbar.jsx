import avatar from "../assets/images/avatar.png";
import { companyLogos } from "../constants/images";
import { useNavigate } from "react-router-dom";

const Navbar = ({ isActive, setIsActive, button }) => {
  const navigate = useNavigate();
  return (
    <div className="pt-10 pb-8 flex flex-col items-center space-y-8">
      <div className="space-y-4">
        <div className="w-30 h-30 rounded-full bg-[#eee] items-center flex justify-center">
          <img src={avatar} alt="Avatar" className="w-20 h-20" />
        </div>
        <h1 className="text-xl text-center text-[#eee]">Hi, Alan</h1>
      </div>
      <div className="flex flex-col w-[100%]">
        {button.map((btn, index) => (
          <div
            key={index}
            onClick={() => {
              setIsActive(btn);
            }}
            className={`p-3 pl-6 ${
              isActive === btn ? "bg-[#f3fdfe]" : ""
            } ml-8 rounded-l-2xl cursor-pointer`}
          >
            <h1
              className={`font-semibold ${
                isActive === btn ? "text-[#192d3c]" : "text-white"
              } `}
            >
              {btn}
            </h1>
          </div>
        ))}
      </div>
      <button
        onClick={() => {
          navigate("/");
        }}
        className="flex justify-center items-center space-x-4 mt-20 p-2 cursor-pointer"
      >
        <h1 className="font-semibold text-white text-lg">Logout</h1>
        <img src={companyLogos.logout} alt="Logout" className="w-7 h-7" />
      </button>
    </div>
  );
};

export default Navbar;
