import os
from flask import Flask, render_template, request, jsonify
from google import genai

# قراءة المفتاح من متغيرات البيئة
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ لم يتم العثور على API Key")

# إنشاء العميل الصحيح
client = genai.Client(api_key=API_KEY)

app = Flask(__name__)

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

        # ✅ الموديل الصحيح المدعوم حاليًا
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_input
        )

        bot_response = response.text.strip()
        print(f"🤖 الرد: {bot_response}")

        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"❌ خطأ داخلي: {e}")
        return jsonify({"error": "حدث خطأ داخلي"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)







