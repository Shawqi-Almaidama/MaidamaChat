import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import errors

# ===============================
# 🔑 API KEY
# ===============================
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY غير موجود")

client = genai.Client(api_key=API_KEY)

# ===============================
# 🔹 Flask
# ===============================
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

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_input
        )

        return jsonify({"response": response.text})

    except errors.ResourceExhausted:
        return jsonify({
            "error": "تم استهلاك الحصة (Quota). انتظر أو فعّل Billing."
        }), 429

    except errors.ClientError as e:
        return jsonify({
            "error": f"خطأ من Gemini API: {e.message}"
        }), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
















