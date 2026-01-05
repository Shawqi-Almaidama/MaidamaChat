import os
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

models = genai.list_models().models

print("✅ النماذج المدعومة بالضبط:")
for m in models:
    print(m.name)

