import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ لم يتم العثور على API Key")

genai.configure(api_key=API_KEY)

app = Flask(__name__)

# ✅ موديل مدعوم رسميًا
model = genai.GenerativeModel("models/text-bison-001")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message", "").strip()
        if not user_input:
            return jsonify({"error": "الرسالة فارغة"}), 400

        print(f"✅ استلام رسالة: {user_input}")

        response = model.generate_content(user_input)
        bot_response = response.text or "لم أتمكن من الرد."

        print(f"🤖 الرد: {bot_response}")

        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"❌ خطأ داخلي: {e}")
        return jsonify({"error": "حدث خطأ داخلي"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)





