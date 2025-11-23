import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Warning: GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=API_KEY)

# Use a standard model
MODEL_NAME = "gemini-2.0-flash" 

def generate_response(prompt: str, system_instruction: str = None) -> str:
    """
    Generates a response from Gemini.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME, system_instruction=system_instruction)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return "I apologize, but I'm having trouble connecting to my brain right now. Please try again."
