import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

WHATSAPP_API_URL = "https://waba.360dialog.io/v1/messages"
API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")

@app.route("/", methods=["GET"])
def health():
    return "Webhook OK", 200

@app.route("/webhook", methods=["POST"])
def receive_message():
    try:
        raw_data = request.data
        print("📦 Corpo grezzo ricevuto:", raw_data)

        data = request.get_json(silent=True)
        print("✅ Payload JSON decodificato:", data)

        if not data:
            print("❌ Nessun dato JSON valido.")
            return jsonify({"error": "No JSON received"}), 400

        messages = data.get("messages", [])
        print(f"📩 Messaggi trovati: {messages}")

        for message in messages:
            from_number = message.get("from")
            print(f"➡️ Numero mittente: {from_number}")
            if from_number:
                send_auto_reply(from_number)

        return jsonify({"status": "received"}), 200

    except Exception as e:
        print("❗ Errore durante la gestione del messaggio:", str(e))
        return jsonify({"error": str(e)}), 500

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

    try:
        response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)
        print("📤 Inviato a:", to)
        print("🔁 Status code:", response.status_code)
        print("📨 Risposta API:", response.text)
    except Exception as e:
        print("❌ Errore nell'invio del messaggio:", str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
