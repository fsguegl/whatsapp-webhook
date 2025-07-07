from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

WHATSAPP_API_URL = "https://waba.360dialog.io/v1/messages"
API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")

@app.route("/", methods=["GET"])
def health():
    return "Webhook OK", 200

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    messages = data.get("messages", [])
    if messages:
        for message in messages:
            from_number = message.get("from")
            if from_number:
                send_auto_reply(from_number)
    return jsonify({"status": "received"}), 200

def send_auto_reply(to):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": to,
        "type": "text",
        "text": {
            "body": "Questo numero è abilitato solo alle comunicazioni in uscita."
        }
    }
    requests.post(WHATSAPP_API_URL, json=payload, headers=headers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
