import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Support multiple API keys - add as many as you want!
API_KEYS = [
    os.getenv("GEMINI_API_KEY"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
]

# Filter out None values (keys that don't exist)
API_KEYS = [key for key in API_KEYS if key]

if not API_KEYS:
    print("Warning: No GEMINI_API_KEY found in environment variables.")

current_key_index = 0
MODEL_NAME = "gemini-2.0-flash"

def generate_response(prompt: str, system_instruction: str = None) -> str:
    """
    Generates a response from Gemini with automatic key rotation on rate limit.
    """
    global current_key_index
    
    for attempt in range(len(API_KEYS)):
        try:
            # Configure with current key
            genai.configure(api_key=API_KEYS[current_key_index])
            
            model = genai.GenerativeModel(MODEL_NAME, system_instruction=system_instruction)
            response = model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            error_msg = str(e)
            
            # Check if it's a rate limit error
            if "quota" in error_msg.lower() or "rate limit" in error_msg.lower() or "429" in error_msg:
                print(f"Rate limit hit on key {current_key_index + 1}. Switching to next key...")
                
                # Switch to next key
                current_key_index = (current_key_index + 1) % len(API_KEYS)
                
                # If we've tried all keys, give up
                if attempt == len(API_KEYS) - 1:
                    print("All API keys have hit rate limits!")
                    return "I apologize, but all API keys have reached their daily limits. Please try again tomorrow or add more API keys."
                
                # Try next key
                continue
            else:
                # Other error, not rate limit
                print(f"Error calling Gemini: {e}")
                return "I apologize, but I'm having trouble connecting right now. Please try again."
    
    return "Unable to generate response after trying all available keys."
