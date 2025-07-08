from flask import Flask, request
import requests
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

WHATSAPP_API_URL = "https://waba-v2.360dialog.io/messages"
API_TOKEN = os.environ.get("WHATSAPP_API_TOKEN")  # <-- assicurati che la variabile sia corretta nel pannello Render

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    logging.info(f"📥 Payload ricevuto: {data}")

    contacts = data.get("contacts")
    messages = data.get("messages")

    if not contacts or not messages:
        logging.info("⚠️ Contatti o messaggi mancanti nel payload")
        return "Missing fields", 200

    phone_number = contacts[0].get("wa_id")
    if not phone_number:
        logging.info("⚠️ Numero WhatsApp non trovato")
        return "Missing phone number", 200

    # Costruzione del corpo per invio template
    payload = {
        "to": phone_number,
        "type": "template",
        "template": {
            "name": "risposta_automatica",
            "language": {
                "code": "it"
            }
        }
    }

    headers = {
        "D360-API-KEY": API_TOKEN,
        "Content-Type": "application/json"
    }

    logging.info(f"📤 Invio template a: {phone_number}")
    response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)
    logging.info(f"✅ Status: {response.status_code}")
    logging.info(f"📬 Response: {response.text}")

    return "ok", 200

@app.route("/", methods=["GET"])
def index():
    return "Webhook attivo 🚀", 200
