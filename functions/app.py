from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from flask import Response

# تهيئة API Key
API_KEY = "AIzaSyDwdzbCrSJjWXMvUQ0e-KO52bYdd71w4_s"
genai.configure(api_key=API_KEY)

# إنشاء تطبيق Flask
app = Flask(__name__)

# التأكد من عمل النموذج باستخدام الإصدار الصحيح
try:
    model = genai.GenerativeModel("gemini-1.5-pro")  # تأكد من استخدام الإصدار الصحيح!
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

# دالة Netlify Functions لتشغيل التطبيق
def handler(request):
    # يستخدم Netlify Functions لتوجيه الطلبات إلى تطبيق Flask
    return app(request)


