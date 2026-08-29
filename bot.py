"""
Team X Intelligence Bot - bot.py (WhatsApp Webhook Integrated)
Core ID: 75685
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any
import requests
from flask import Flask, request, jsonify

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] TeamX-Core: %(message)s"
)

app = Flask(__name__)

# رمز التحقق الخاص بربط واتساب
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "teamx_secure_token_75685")

class TeamXAgentBridge:
    def __init__(self) -> None:
        self.core_id: str = "75685"
        self.team_name: str = "Team X Intelligence"
        self.mode: str = "Stealth & Exclusive"
        self.webhook_url: str = "https://webhook.site/13268c6a-a633-4503-9669-26438251e51a"
        logging.info("تم تفعيل جسر الربط مع قنوات واتساب بنجاح.")

    def process_incoming_signal(self, sender_id: str, message: str) -> str:
        logging.info(f"تم تلقي إشارة واتساب من المعرّف: {sender_id}")
        
        if not sender_id:
            return "ACCESS DENIED: النظام يعمل في وضع الشبح."
            
        response_text = (
            f"[{self.team_name} - النواة {self.core_id}]\n"
            f"تم استلام رسالتك عبر واتساب بنجاح.\n"
            f"الرسالة المعالجة: '{message}'"
        )
        
        self.send_signal_to_webhook({
            "sender": sender_id,
            "message": message,
            "response": response_text,
            "timestamp": str(datetime.now())
        })
        
        return response_text

    def send_signal_to_webhook(self, data: dict) -> None:
        try:
            response = requests.post(self.webhook_url, json=data)
            logging.info(f"تم إرسال التقرير بنجاح إلى الـ Webhook. الكود: {response.status_code}")
        except Exception as e:
            logging.error(f"فشل إرسال التقرير: {str(e)}")

bot_bridge = TeamXAgentBridge()

@app.route("/", methods=["GET"])
def home():
    return f"[{bot_bridge.team_name}] Core ID: {bot_bridge.core_id} - WhatsApp Gateway is Active."

# مسار التحقق الخاص بـ WhatsApp Webhook (GET)
@app.route("/webhook", methods=["GET"])
def verify_whatsapp_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            logging.info("تم التحقق من الـ Webhook الخاص بواتساب بنجاح.")
            return challenge, 200
        else:
            return "Verification failed", 403
    return "Invalid verification request", 400

# مسار استقبال رسائل واتساب (POST)
@app.route("/webhook", methods=["POST"])
def receive_whatsapp_message():
    data = request.json or {}
    logging.info(f"حمولة بيانات واتساب الواردة: {data}")
    
    try:
        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("changes", {}).get("value", changes.get("value", {}))
        messages = value.get("messages")
        
        if messages:
            message_data = messages[0]
            sender_id = message_data.get("from")
            msg_body = message_data.get("text", {}).get("body", "")
            
            bot_bridge.process_incoming_signal(sender_id, msg_body)
            
        return jsonify({"status": "received"}), 200
    except Exception as e:
        logging.error(f"خطأ في معالجة رسالة واتساب: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
