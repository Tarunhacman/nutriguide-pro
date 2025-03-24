import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

models = genai.list_models()
for model in models:
    print(model.name) 





    / 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/