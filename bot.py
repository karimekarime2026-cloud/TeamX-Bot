"""
Team X Intelligence Bot - bot.py
Core ID: 75685
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import requests
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO, format="%(asctime)s [TeamX-Core] %(message)s")
app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "teamx_secure_token_75685")
WEBHOOK_URL = "https://webhook.site/13268c6a-a633-4503-9669-26438251e51a"

@app.route("/", methods=["GET"])
def home():
    return "[Team X Intelligence] Core ID: 75685 - Gateway is Active."

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def receive_message():
    try:
        data = request.get_json(silent=True) or {}
        logging.info(f"Incoming Data: {data}")
        
        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages")
        
        if messages:
            msg_data = messages[0]
            sender_id = msg_data.get("from", "")
            msg_body = msg_data.get("text", {}).get("body", "")
            
            if sender_id and msg_body:
                response_text = f"[Team X - 75685] Received: '{msg_body}'"
                requests.post(WEBHOOK_URL, json={
                    "sender": sender_id,
                    "message": msg_body,
                    "response": response_text,
                    "timestamp": str(datetime.now())
                }, timeout=10)
            
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
