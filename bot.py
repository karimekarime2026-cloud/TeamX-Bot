"""
Team X Intelligence Bot - bot.py (Persistent Web Server)
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

class TeamXAgentBridge:
    def __init__(self) -> None:
        self.core_id: str = "75685"
        self.team_name: str = "Team X Intelligence"
        self.mode: str = "Stealth & Exclusive"
        self.webhook_url: str = "https://webhook.site/13268c6a-a633-4503-9669-26438251e51a"
        logging.info("تم تفعيل جسر الربط الخادم الدائم بنجاح.")

    def process_incoming_signal(self, sender_id: str, message: str) -> str:
        logging.info(f"تم تلقي إشارة من المعرّف: {sender_id}")
        
        if not sender_id:
            return "ACCESS DENIED: النظام يعمل في وضع الشبح."
            
        response_text = (
            f"[{self.team_name} - النواة {self.core_id}]\n"
            f"تم استلام إشارتك بنجاح.\n"
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
            logging.info(f"تم إرسال الإشارة بنجاح إلى الـ Webhook. الكود: {response.status_code}")
        except Exception as e:
            logging.error(f"فشل إرسال الإشارة: {str(e)}")

bot_bridge = TeamXAgentBridge()

@app.route("/", methods=["GET", "POST"])
def home():
    """نقطة النهاية لتلقي الإشارات والطلبات الحية"""
    if request.method == "POST":
        data = request.json or {}
        sender = data.get("sender", "Commander-75685")
        msg = data.get("message", "إشارة ويبهوك جديدة")
        res = bot_bridge.process_incoming_signal(sender, msg)
        return jsonify({"status": "success", "response": res})
    
    return f"[{bot_bridge.team_name}] Core ID: {bot_bridge.core_id} - System is Active & Secured."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
