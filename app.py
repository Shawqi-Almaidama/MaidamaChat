import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# الحصول على API Key من متغيرات البيئة بدلاً من تضمينه في الكود
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ لم يتم العثور على API Key في متغيرات البيئة.")

genai.configure(api_key=API_KEY)

# إنشاء تطبيق Flask
app = Flask(__name__)

# التأكد من عمل النموذج باستخدام الإصدار الصحيح
try:
    model = genai.GenerativeModel("gemini-1.5-pro")
except Exception as e:
    print(f"❌ خطأ في تحميل النموذج: {str(e)}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message", "").strip()
        if not user_input:
            return jsonify({"error": "الرسالة فارغة"}), 400

        print(f"✅ استلام رسالة: {user_input}")  # طباعة الإدخال في Terminal
        
        response = model.generate_content(user_input)
        bot_response = response.text.strip() if hasattr(response, "text") else "عذرًا، لم أفهم سؤالك."

        print(f"🤖 استجابة البوت: {bot_response}")  # طباعة استجابة البوت
        
        return jsonify({"response": bot_response})
    except Exception as e:
        print(f"❌ خطأ داخلي: {str(e)}")  # طباعة الخطأ في Terminal
        return jsonify({"error": "حدث خطأ داخلي، يرجى المحاولة لاحقًا"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))


