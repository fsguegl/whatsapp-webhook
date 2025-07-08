import os
import logging
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configura logging
logging.basicConfig(level=logging.INFO)

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
                logging.info(f"Ricevuto messaggio da: {from_number}")
                send_auto_reply(from_number)
    else:
        logging.info("Nessun messaggio ricevuto nel payload.")
    return jsonify({"status": "received"}), 200

def send_auto_reply(to):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
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

    response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)

    logging.info(f"Invio messaggio a {to} - Status: {response.status_code}")
    logging.info(f"Risposta API: {response.text}")

if __name__ == "__main__":
    # Attiva modalità debug
    app.run(host="0.0.0.0", port=10000, debug=True)
