export async function chatWithAgent(text) {
  try {
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    return data.response; // trả về text từ backend
  } catch (err) {
    console.error("Error calling backend:", err);
    return "Backend error";
  }
}
