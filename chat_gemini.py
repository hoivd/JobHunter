import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

# Khởi tạo model
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash-lite",
    google_api_key=google_api_key
    )
response = llm.invoke("Sing a ballad of LangChain.")
print(response)

#