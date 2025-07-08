import os
import logging
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Abilita log su console
logging.basicConfig(level=logging.INFO)

# Recupera il token API da Render (variabile ambiente)
API_TOKEN = os.environ.get("WHATSAPP_API_TOKEN")
WHATSAPP_API_URL = "https://waba-v2.360dialog.io/messages"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    logging.info("▶️ Payload ricevuto:")
    logging.info(data)

    if not data:
        return jsonify({"error": "No data received"}), 400

    contacts = data.get("contacts", [])
    messages = data.get("messages", [])

    if not contacts or not messages:
        logging.warning("⚠️ Contatti o messaggi mancanti nel payload")
        return jsonify({"status": "ignored"}), 200

    phone_number = contacts[0].get("wa_id")
    logging.info(f"📱 Numero WhatsApp: {phone_number}")

    # Invia il template "risposta_automatica"
 headers = {
    "D360-API-KEY": API_TOKEN,
    "Content-Type": "application/json"
}

payload = {
    "to": phone_number,
    "type": "template",
    "template": {
        "namespace": "your_template_namespace",  # <-- aggiorna se serve
        "name": "risposta_automatica",
        "language": {
            "code": "it"
        }
    }
}

response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)

    try:
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        logging.info(f"📤 Inviato template a {phone_number}")
        logging.info(f"✅ Status: {response.status_code}")
        logging.info(f"📝 Response: {response.text}")
    except Exception as e:
        logging.error(f"❌ Errore durante l'invio: {e}")

    return jsonify({"status": "received"}), 200

@app.route("/", methods=["GET"])
def home():
    return "✅ Webhook online"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
