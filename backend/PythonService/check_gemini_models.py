import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("GEMINI_API_KEY not found")
    exit(1)

genai.configure(api_key=api_key)

try:
    models = []
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            models.append({
                "name": model.name,
                "display_name": model.display_name,
                "description": model.description
            })
    print(f"Total Gemini models: {len(models)}")
    for model in models:
        print(f"- {model['name']} ({model['display_name']})")
except Exception as e:
    print(f"Error: {e}")
