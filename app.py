import logging
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import requests

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

# ==========================================
# إعدادات نظام المراقبة والسجلات الاحترافية
# ==========================================
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# جلب مفتاح الـ API بأمان من متغيرات البيئة
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
# استخدام النطاق الرسمي والمحدث لضمان سرعة الاستجابة وعدم التعليق
COHERE_API_URL = "https://api.cohere.com/v1/chat"

# إدارة جلسة المحادثة والذاكرة
session_history = []
MAX_HISTORY_LENGTH = 10


def get_ai_response(user_message: str) -> str:
  global session_history

  headers = {
      "accept": "application/json",
      "content-type": "application/json",
      "Authorization": f"Bearer {COHERE_API_KEY}",
  }

  payload = {
      "message": user_message,
      "chat_history": session_history,
      "preamble": (
          "You are an elite, highly intelligent AI assistant. "
          "Respond accurately, professionally, and concisely. "
          "CRITICAL: Match the user's language exactly. If the user speaks Arabic, reply in Arabic. If English, reply in English."
      ),
      "temperature": 0.3,
  }

  try:
    logger.info("Sending request to official Cohere API endpoint...")
    # رفع المهلة إلى 30 ثانية لمنع حدوث أي Timeout نهائياً
    response = requests.post(
        COHERE_API_URL, json=payload, headers=headers, timeout=30
    )

    if response.status_code != 200:
      try:
        error_data = response.json()
        error_msg = error_data.get("message", "خطأ غير معروف")
      except:
        error_msg = response.text

      logger.error(f"API Error [{response.status_code}]: {error_msg}")
      return f"عذراً، خطأ من الخادم: {error_msg}"

    data = response.json()
    reply = data.get("text", "")

    if not reply.strip():
      logger.warning("Received empty response from the model.")
      return "عذراً، لم أتمكن من صياغة إجابة مناسبة."

    # تحديث الذاكرة بنجاح
    session_history.append({"role": "USER", "message": user_message})
    session_history.append({"role": "CHATBOT", "message": reply})

    if len(session_history) > MAX_HISTORY_LENGTH * 2:
      session_history = session_history[-(MAX_HISTORY_LENGTH * 2) :]

    logger.info("Response received and processed successfully.")
    return reply

  except requests.exceptions.Timeout:
    logger.error("Request timed out after 30 seconds.")
    return "استغرق الخادم وقتاً أطول من اللازم. يرجى المحاولة لاحقاً."

  except requests.exceptions.ConnectionError:
    logger.error("Connection error to cohere.com.")
    return "فشل الاتصال بخوادم الذكاء الاصطناعي. يرجى التحقق من شبكة الإنترنت."

  except Exception as e:
    logger.error(f"Unexpected System Error: {str(e)}")
    return "حدث خطأ داخلي غير متوقع في معالجة الطلب."


@app.route("/api/chat", methods=["POST"])
def chat_endpoint():
  try:
    data = request.get_json()

    if not data or "message" not in data:
      return (
          jsonify({"status": "error", "message": "بيانات الطلب غير صالحة."}),
          400,
      )

    user_message = data["message"].strip()

    if not user_message:
      return jsonify({"status": "error", "message": "الرسالة فارغة."}), 400

    bot_response = get_ai_response(user_message)

    return jsonify({"status": "success", "reply": bot_response}), 200

  except Exception as e:
    logger.critical(f"Endpoint Fatal Error: {str(e)}")
    return (
        jsonify({"status": "error", "message": "تعطلت معالجة الطلب في الخادم."}),
        500,
    )


# أضف هذا المسار لخدمة ملف index.html الرئيسي
@app.route("/")
def serve_index():
  return send_from_directory(".", "index.html")


if __name__ == "__main__":
  print("🚀 بدء تشغيل خادم الذكاء الاصطناعي النسخة النهائية المستقرة...")
  app.run(host="0.0.0.0", port=5000, debug=False)
