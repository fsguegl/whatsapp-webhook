import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

WHATSAPP_API_URL = "https://waba.360dialog.io/v1/messages"
API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")  # Assicurati che sia settato su Render

@app.route("/", methods=["GET"])
def health():
    return "Webhook OK", 200

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    print("✅ Webhook payload ricevuto:", data)  # DEBUG

    messages = data.get("messages", [])
    if messages:
        for message in messages:
            from_number = message.get("from")
            print("📩 Numero mittente:", from_number)  # DEBUG
            if from_number:
                send_auto_reply(from_number)
            else:
                print("⚠️ 'from' mancante nel messaggio")  # DEBUG
    else:
        print("⚠️ Nessun messaggio trovato nel payload")  # DEBUG

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

    print("➡️ Inviando template a:", to)
    print("📦 Payload:", payload)

    response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)

    print("✅ Status code:", response.status_code)
    print("📨 Risposta API:", response.text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
