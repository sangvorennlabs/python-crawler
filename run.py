from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
import os


llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_kwargs={
      "extra_headers":{
        "Helicone-Auth": f"Bearer {os.getenv('HELICONE_API_KEY')}",
        "Helicone-User-Id": "alicebob@gmail.com",
        "Helicone-Property-Session": "1234567890",
        "Helicone-Property-UserAge": "18",
      }
    },
    openai_api_base="https://oai.helicone.ai/v1",
)

llm.invoke("Hello, how are you?")
