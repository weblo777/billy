import openai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY", "")

model = "gpt-3.5-turbo-16k"
client = openai.OpenAI(
    api_key=api_key,
)
