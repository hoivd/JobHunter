import { useState } from "react";
import { user, password, close } from "../../constants/icons";
import { useNavigate } from "react-router-dom";
import { initializeApp } from "firebase/app";
import { getAuth, signInWithEmailAndPassword } from "@firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyB-qTS5qiHHwASdEgUomIDurZCsv27SP44",
  authDomain: "jobhuntx-fae03.firebaseapp.com",
  projectId: "jobhuntx-fae03",
  storageBucket: "jobhuntx-fae03.firebasestorage.app",
  messagingSenderId: "732095170571",
  appId: "1:732095170571:web:e354951acaf7ca17729f0e",
  measurementId: "G-1TZ5SBXXK9",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const Signin = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [pass, setPass] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async () => {
    setLoading(true);
    setError("");
    try {
      await signInWithEmailAndPassword(auth, email, pass);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="w-full h-screen flex flex-col justify-center items-center"
      style={{
        background:
          "linear-gradient(45deg,rgba(25, 51, 90, 1) 10%, rgba(165, 184, 232, 1) 92%)",
      }}
    >
      <div className="w-[40%] h-[65%] flex flex-col justify-center items-center">
        <div className="w-[80%] h-[70%] bg-white/40 p-8 rounded-2xl shadow-[0_0_9px_0px_rgba(0,0,0,0.25)] relative">
          <div
            onClick={() => {
              navigate("/");
            }}
            className="self-end hover:cursor-pointer absolute top-6 right-6"
          >
            <img src={close} alt="Close sign up" className="w-4 h-4" />
          </div>
          <h1 className="text-center font-semibold text-3xl my-6 text-[#19335A]">
            Sign in
          </h1>
          <div className="flex items-center justify-center p-5 rounded-full bg-[#19335A] w-26 h-26 absolute -top-14 left-[calc(50%-48px)] shadow-[0_0_10px_0px_rgba(0,0,0,0.25)]">
            <img src={user} alt="Account" className="w-20" />
          </div>

          <div className="flex flex-col items-center space-y-6  w-full h-[70%]">
            {/* Email */}
            <div className="grid grid-cols-[10%_80%] w-[90%] h-[25%] bg-white/90 shadow-[0_0_9px_0px_rgba(0,0,0,0.25)]">
              <div className="flex justify-center items-center bg-[#19335A] w-full h-full">
                <img src={user} alt="User" className="w-5" />
              </div>
              <input
                type="email"
                placeholder="Email ID"
                className="focus:outline-none focus:ring-0 px-4"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            {/* Password */}
            <div className="grid grid-cols-[10%_80%] w-[90%] h-[25%] bg-white/90 shadow-[0_0_9px_0px_rgba(0,0,0,0.25)]">
              <div className="flex justify-center items-center bg-[#19335A] w-full h-full">
                <img src={password} alt="Password" className="w-5" />
              </div>
              <input
                type="password"
                placeholder="Password"
                className="focus:outline-none focus:ring-0 px-4"
                value={pass}
                onChange={(e) => setPass(e.target.value)}
              />
            </div>

            <p className="flex justify-end w-[90%] underline text-[#19335A] cursor-pointer">
              Forgot password?
            </p>
          </div>
          {error && (
            <p className="text-red-600 text-center text-sm mt-2">{error}</p>
          )}
        </div>
      </div>

      <div
        onClick={handleLogin}
        className="w-[28%] h-[8%] bg-white/20 absolute top-116 rounded-b-4xl flex justify-center items-center cursor-pointer shadow-[0_0_9px_0px_rgba(0,0,0,0.25)] hover:brightness-110 hover:scale-105 hover:shadow-[0_0_15px_0px_rgba(0,0,0,0.35)] transition-all duration-300"
      >
        {loading ? (
          <h1 className="font-semibold text-xl text-white animate-pulse">
            Loading...
          </h1>
        ) : (
          <h1 className="font-semibold text-xl text-white">Login</h1>
        )}
      </div>
    </div>
  );
};

export default Signin;
