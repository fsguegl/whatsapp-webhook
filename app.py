import os
from flask import Flask, request
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Token API salvato come variabile di ambiente in Render
API_TOKEN = os.environ.get("WHATSAPP_API_TOKEN")
WHATSAPP_API_URL = "https://waba-v2.360dialog.io/messages"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    logging.info("📩 Payload ricevuto: %s", data)

    # Estrai i dati dal messaggio ricevuto
    messages = data.get("messages")
    contacts = data.get("contacts")

    if messages and contacts:
        phone_number = contacts[0].get("wa_id")
        logging.info("📞 Numero WhatsApp: %s", phone_number)

        # Costruzione del payload per il template WhatsApp
        payload = {
            "to": phone_number,
            "type": "template",
            "template": {
                "namespace": "your_template_namespace",  # opzionale, se richiesto
                "name": "risposta_automatica",
                "language": {
                    "code": "it"
                }
            }
        }

        # Header richiesto da 360dialog
        headers = {
            "D360-API-KEY": API_TOKEN,
            "Content-Type": "application/json"
        }

        # Invio della richiesta
        try:
            response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
            logging.info("📤 Inviato template a %s", phone_number)
            logging.info("✅ Status: %s", response.status_code)
            logging.info("🔁 Response: %s", response.json())
        except Exception as e:
            logging.error("❌ Errore nell'invio del messaggio: %s", str(e))
    else:
        logging.warning("⚠️ Contatti o messaggi mancanti nel payload")

    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "Webhook attivo!", 200

if __name__ == "__main__":
    app.run(debug=True, port=10000)
