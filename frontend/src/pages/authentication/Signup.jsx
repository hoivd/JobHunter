import { companyLogos } from "../../constants/images";
import { close } from "../../constants/icons";
import { useNavigate } from "react-router-dom";

const Signup = () => {
  const navigate = useNavigate();
  return (
    <div
      className="w-full h-screen flex flex-col justify-center items-center"
      style={{
        background:
          "linear-gradient(195deg,rgba(25, 51, 90, 1) 10%, rgba(165, 184, 232, 1) 90%)",
      }}
    >
      <div className="relative h-[90%] flex justify-center items-center w-[80%]">
        <img
          src={companyLogos.bg}
          alt="Road to your future life"
          className="rounded-2xl shadow-2xl object-cover object-center h-[80%]"
        />
        <div className="absolute z-20 top-35 left-60 flex flex-col justify-center space-y-6">
          <h1 className=" text-[#19335A] text-8xl font-black tracking-wide">
            Sign <br /> up
          </h1>
          <p className="text-white text-lg">
            Create an account <br /> to get a dream job
          </p>
        </div>
        <div className="absolute z-10 top-18 right-40 w-[40%] h-[75%] rounded-2xl flex flex-col bg-white/30 shadow-xl py-4 px-8">
          <div
            onClick={() => {
              navigate("/");
            }}
            className="w-8 h-8 rounded-full bg-[#a5b8e8] flex justify-center items-center cursor-pointer hover:brightness-110 hover:scale-105 hover:shadow-[0_0_15px_0px_rgba(0,0,0,0.35)] transition-all duration-300 self-end"
          >
            <img src={close} alt="Close sign up" className="w-4 h-4" />
          </div>
          <div className="flex flex-col space-y-3 mt-10 w-full h-[50%]">
            <h1 className="text-lg font-semibold text-black/80">Email ID</h1>
            <form className="grid grid-cols-1 rounded-2xl w-[90%] h-[20%] bg-white/80 border-b-white/90 shadow-[0_0_9px_0px_rgba(0,0,0,0.25)] ">
              <input
                type="text"
                placeholder="Email ID"
                className="focus:outline-none focus:ring-0 px-4"
              />
            </form>
            <h1 className="text-lg font-semibold text-black/85">Password</h1>
            <form className="grid grid-cols-1 rounded-2xl w-[90%] h-[20%] bg-white/80 shadow-[0_0_9px_0px_rgba(0,0,0,0.25)] ">
              <input
                type="text"
                placeholder="Password"
                className="focus:outline-none focus:ring-0 px-4"
              />
            </form>
          </div>
          <div className="self-center w-[40%] py-2 rounded-2xl bg-[#19335A] flex justify-center items-center mt-4 cursor-pointer hover:brightness-110 hover:scale-105 hover:shadow-[0_0_15px_0px_rgba(0,0,0,0.35)] transition-all duration-300">
            <h1 className="font-semibold text-white text-lg">Sign up</h1>
          </div>
          <h1 className="mt-4 text-center cursor-pointer text-[#19335a] hover:underline">
            Already have account?
          </h1>
        </div>
      </div>
    </div>
  );
};

export default Signup;
