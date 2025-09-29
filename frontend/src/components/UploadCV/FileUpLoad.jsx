import { useState } from "react";
import { companyLogos } from "../../constants/images";
import { motion } from "framer-motion";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [isUpload, setIsUpload] = useState(false);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected && selected.type === "application/pdf") {
      setFile(selected);
      uploadFile(selected);
    } else {
      alert("Chỉ được upload file PDF!");
    }
  };

  const uploadFile = (file) => {
    setIsUploading(true);
    setProgress(0);

    // Fake upload progress
    const total = file.size;
    let uploaded = 0;
    const interval = setInterval(() => {
      uploaded += total / 100;
      const percent = Math.min(Math.round((uploaded / total) * 100), 100);
      setProgress(percent);
      if (percent === 100) {
        clearInterval(interval);
        setIsUploading(false);
      }
    }, 100);
  };

  return (
    <div className=" mx-auto h-full rounded-xl p-4 text-center flex flex-col items-center justify-center">
      {isUpload === true ? (
        <>
          <motion.div
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="flex flex-col items-center mt-6"
          >
            <img
              src={companyLogos.check}
              alt="Uploaded file"
              className="w-26"
            />
            <h1 className="text-2xl font-semibold mt-4 ">
              File successfully <span className="text-[#39bffe]">uploaded</span>
            </h1>
          </motion.div>
        </>
      ) : (
        <>
          <h2 className="text-2xl font-semibold mb-8 text-[#19335a]">
            Upload your CV.pdf
          </h2>
          <label
            htmlFor="fileInput"
            className="border-2 border-dashed border-gray-300 rounded-lg p-6 cursor-pointer flex flex-col items-center justify-center"
          >
            <img src={companyLogos.pdf} alt="Upload CV" className="w-30" />
            <p className="text-gray-500">Drag & Drop hoặc click để chọn file</p>
            <input
              id="fileInput"
              type="file"
              accept="application/pdf"
              className="hidden"
              onChange={handleFileChange}
            />
          </label>
          <div className="w-full h-full flex space-x-8 px-4">
            {file && (
              <div className="mt-4 flex items-center gap-4 w-full">
                {/* Tên file */}
                <div className="max-w-[40%] break-words text-sm font-medium text-left">
                  {file.name}
                </div>

                {/* Progress bar */}
                <div className="flex items-center gap-2 w-full max-w-[50%]">
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="h-2 rounded-full"
                      style={{
                        background:
                          "linear-gradient(to left, #19335a, #697a98)",
                        width: `${progress}%`,
                      }}
                    ></div>
                  </div>
                  {/* % căn ngay cạnh bar */}
                  <p className="text-sm min-w-[40px] text-right">{progress}%</p>
                </div>
              </div>
            )}

            {progress === 100 && (
              <button
                onClick={() => setIsUpload(true)}
                className="mt-4 px-6 py-2 text-white rounded-lg font-semibold cursor-pointer bg-green-500"
              >
                Upload
              </button>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default FileUpload;
