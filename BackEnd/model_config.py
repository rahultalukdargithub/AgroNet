from authorization import authorization
import google.generativeai as genai
# Load environment variables
api_key = authorization.API_KEY

if not api_key:
    raise ValueError("API_KEY not set in environment variables.")

# Configure generative AI with API key
genai.configure(api_key=api_key)

# Safety settings for the generative model
gemini_safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]
generation_configuration = {
    "temperature": 0.75,
    "top_p": 0.5,
    "max_output_tokens": 2048,
    "top_k": 40,
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=gemini_safety_settings,
)