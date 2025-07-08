import os
import logging
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configurazione log
logging.basicConfig(level=logging.INFO)

# Costanti
WHATSAPP_API_URL = "https://waba.360dialog.io/v1/messages"
API_KEY = os.getenv("WHATSAPP_API_TOKEN")

@app.route("/", methods=["GET"])
def health():
    return "Webhook OK", 200

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    logging.info("📩 Payload ricevuto: %s", data)

    messages = data.get("messages", [])
    contacts = data.get("contacts", [])

    if messages and contacts:
        for message in messages:
            from_number = message.get("from")
            logging.info("☎️ Numero WhatsApp: %s", from_number)
            if from_number:
                send_auto_reply(from_number)
    else:
        logging.warning("⚠️ Contatti o messaggi mancanti nel payload")

    return jsonify({"status": "received"}), 200

def send_auto_reply(to):
    headers = {
        "D360-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": "risposta_automatica",
            "language": {
                "code": "it"
            }
        }
    }

    response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)

    logging.info("📨 Inviato template a: %s", to)
    logging.info("✅ Status: %s", response.status_code)
    logging.info("📡 Response: %s", response.text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
