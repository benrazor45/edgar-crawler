from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv('.env')
gemini_api_key = os.getenv('GEMINI_API_KEY')

client = genai.Client()
prompt = "Explain the concept of Occam's Razor and provide a simple, everyday example."
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=prompt
)

print(response.text)