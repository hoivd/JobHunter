import { useState } from "react";

const LiveLatex = () => {
  const [latex, setLatex] = useState("");
  const [pdfBase64, setPdfBase64] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const compileLatex = async () => {
    if (!latex) return;

    setLoading(true);
    setError("");
    const formData = new FormData();
    formData.append("latex", latex);

    try {
      const res = await fetch("http://localhost:8000/compile_latex/", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();

      if (data.pdf_base64) {
        setPdfBase64(data.pdf_base64);
      } else if (data.error) {
        setError(data.error);
        setPdfBase64("");
      }
    } catch (err) {
      setError(err.message);
      setPdfBase64("");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Left: textarea */}
      <div style={{ width: "50%", padding: "10px" }}>
        <textarea
          value={latex}
          onChange={(e) => setLatex(e.target.value)}
          placeholder="Nhập LaTeX..."
          style={{ width: "100%", height: "90%", fontSize: "16px" }}
        />
        <button
          onClick={compileLatex}
          style={{
            marginTop: "10px",
            padding: "10px 20px",
            fontSize: "16px",
            cursor: "pointer",
          }}
          disabled={loading}
        >
          {loading ? "Compiling..." : "Compile"}
        </button>
        {error && (
          <div style={{ color: "red", marginTop: "10px" }}>Error: {error}</div>
        )}
      </div>

      {/* Right: PDF viewer */}
      <div style={{ width: "50%", borderLeft: "1px solid gray" }}>
        {pdfBase64 ? (
          <iframe
            title="PDF preview"
            src={`data:application/pdf;base64,${pdfBase64}`}
            style={{ width: "100%", height: "100%" }}
          />
        ) : (
          <p style={{ textAlign: "center", marginTop: "50%" }}>
            PDF sẽ hiển thị ở đây
          </p>
        )}
      </div>
    </div>
  );
};

export default LiveLatex;
