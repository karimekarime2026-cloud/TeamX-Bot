"""
Team X Intelligence Bot - bot.py (Advanced WhatsApp Webhook Gateway)
Core ID: 75685
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import requests
from flask import Flask, request, jsonify

# إعداد السجلات الاحترافية
logging.basicConfig(
   level=logging.INFO,
   format="%(asctime)s [%(levelname)s] TeamX-Core: %(message)s"
)

app = Flask(__name__)

# رمز التحقق الآمن لربط واتساب
VERIFY_TOKEN: str = os.environ.get("VERIFY_TOKEN", "teamx_secure_token_75685")

class TeamXAgentBridge:
   """
   جسر الربط الذكي والمعالج الرئيسي للإشارات الواردة والصادرة.
   """
   def __init__(self) -> None:
       self.core_id: str = "75685"
       self.team_name: str = "Team X Intelligence"
       self.mode: str = "Stealth & Exclusive"
       self.webhook_url: str = "https://webhook.site/13268c6a-a633-4503-9669-26438251e51a"
       logging.info("تم تفعيل النواة وجسر الأمان بنجاح.")

   def process_incoming_signal(self, sender_id: str, message: str) -> str:
       logging.info(f"معالجة إشارة واردة من المعرّف: {sender_id}")
       
       if not sender_id:
           return "ACCESS DENIED: النظام يعمل في وضع الشبح."
           
       response_text = (
           f"[{self.team_name} - النواة {self.core_id}]\n"
           f"تم استقبال رسالتك عبر واتساب بنجاح وتشفيرها.\n"
           f"الرسالة المعالجة: '{message}'"
       )
       
       self.send_signal_to_webhook({
           "sender": sender_id,
           "message": message,
           "response": response_text,
           "timestamp": str(datetime.now())
       })
       
       return response_text

   def send_signal_to_webhook(self, data: Dict[str, Any]) -> None:
       try:
           response = requests.post(self.webhook_url, json=data, timeout=10)
           logging.info(f"تم إرسال التقرير إلى الـ Webhook بنجاح. رمز الحالة: {response.status_code}")
       except requests.exceptions.RequestException as e:
           logging.error(f"فشل إرسال التقرير إلى الـ Webhook: {str(e)}")

bot_bridge = TeamXAgentBridge()

@app.route("/", methods=["GET"])
def home() -> str:
   return f"[{bot_bridge.team_name}] Core ID: {bot_bridge.core_id} - Advanced Gateway is Active & Secured."

# مسار التحقق الخاص بـ WhatsApp Webhook (GET)
@app.route("/webhook", methods=["GET"])
def verify_whatsapp_webhook() -> tuple[str, int]:
   mode: Optional[str] = request.args.get("hub.mode")
   token: Optional[str] = request.args.get("hub.verify_token")
   challenge: Optional[str] = request.args.get("hub.challenge")

   if mode and token:
       if mode == "subscribe" and token == VERIFY_TOKEN:
           logging.info("تم التحقق من تطابق رمز الـ Webhook بنجاح.")
           return challenge or "", 200
       else:
           return "Verification failed: Token mismatch", 403
   return "Invalid verification request parameters", 400

# مسار استقبال رسائل واتساب (POST)
@app.route("/webhook", methods=["POST"])
def receive_whatsapp_message() -> tuple[Any, int]:
   try:
       data: Dict[str, Any] = request.get_json(silent=True) or {}
       logging.info(f"حمولة بيانات واتساب الواردة: {data}")
       
       entry = data.get("entry", [{}])[0]
       changes = entry.get("changes", [{}])[0]
       value = changes.get("value", {})
       messages = value.get("messages")
       
       if messages:
           message_data = messages[0]
           sender_id: str = message_data.get("from", "")
           msg_body: str = message_data.get("text", {}).get("body", "")
           
           if sender_id and msg_body:
               bot_bridge.process_incoming_signal(sender_id, msg_body)
           
       return jsonify({"status": "success", "message": "Signal processed"}), 200
   except Exception as e:
       logging.error(f"خطأ حرج أثناء معالجة رسالة واتساب: {str(e)}")
       return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
   port: int = int(os.environ.get("PORT", 10000))
   app.run(host="0.0.0.0", port=port)
