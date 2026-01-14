import os
from flask import Flask, render_template, request, jsonify
from google import genai

# ===============================
# 🔑 التحقق من مفتاح Gemini API
# ===============================
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ لم يتم العثور على GEMINI_API_KEY في Environment Variables")

# ===============================
# 🎛 إعداد العميل
# ===============================
client = genai.Client(api_key=API_KEY)

# ===============================
# 🔹 إعداد Flask
# ===============================
app = Flask(__name__)

# ===============================
# 🏠 الصفحة الرئيسية
# ===============================
@app.route("/")
def home():
    return render_template("index.html")  # تأكد أن index.html موجود داخل templates/

# ===============================
# 💬 واجهة الدردشة
# ===============================
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message", "").strip()
        if not user_input:
            return jsonify({"error": "الرسالة فارغة"}), 400

        print(f"✅ استلام رسالة من المستخدم: {user_input}")

        # ===============================
        # 🧠 استدعاء Gemini API
        # ===============================
        response = client.models.generate_content(
            model="gemini-2.0-flash",  # ← استخدم الموديل الصحيح الذي ظهر في /list-models
            contents=user_input
        )

        bot_response = response.text.strip()
        print(f"🤖 الرد من Gemini: {bot_response}")

        return jsonify({"response": bot_response})

    except genai.exceptions.GenAIError as ge:
        print(f"❌ خطأ في Gemini API: {ge}")
        return jsonify({"error": "حدث خطأ أثناء الاتصال بـ Gemini API"}), 500

    except Exception as e:
        print(f"❌ خطأ داخلي في السيرفر: {e}")
        return jsonify({"error": "حدث خطأ داخلي في السيرفر"}), 500

# =======================================
# Route مؤقتة لعرض الموديلات المتاحة
# =======================================
@app.route("/list-models")
def list_models():
    try:
        models = client.models.list()
        model_names = [m["name"] for m in models]
        return "<br>".join(model_names)
    except Exception as e:
        return f"❌ خطأ: {e}"

# ===============================
# 🔹 تشغيل التطبيق
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)












