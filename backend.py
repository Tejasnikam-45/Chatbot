import base64
import os
import google.generativeai as genai  # Corrected import
from dotenv import load_dotenv
# Configure API Key
load_dotenv()
genai.configure(api_key= os.getenv("GEMINI_API_KEY"))  # Replace with your actual key

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",  # Consider using an updated model version
    generation_config=generation_config,
)

def GenerateResponse(input_text):
    response = model.generate_content(input_text)  # Fixed input format
    return response.text

# while True:
#     string = input("Enter your prompt: ")
#     print("Bot:", GenerateResponse(string))



