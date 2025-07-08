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
        data = request.get_json()
        print("✅ Payload ricevuto:", data)

        if not data:
            print("❌ Nessun dato JSON ricevuto.")
            return jsonify({"error": "No data received"}), 400

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

    response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)
    print(f"📤 Inviato a {to} | Status: {response.status_code}")
    print("📨 Risposta:", response.text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
