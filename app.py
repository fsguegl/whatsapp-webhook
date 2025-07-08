import os
import sys
import requests
from flask import Flask, request, jsonify

# Forza la stampa immediata nel log Render
sys.stdout.reconfigure(line_buffering=True)

app = Flask(__name__)

WHATSAPP_API_URL = "https://waba-v2.360dialog.io/messages"
API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")  # Ricordati di aggiornarlo in Render

@app.route("/", methods=["GET"])
def health():
    return "Webhook OK", 200

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    print("📥 Ricevuto messaggio:", data, flush=True)

    try:
        contacts = data.get("contacts", [])
        messages = data.get("messages", [])
        if contacts and messages:
            wa_id = contacts[0].get("wa_id")
            if wa_id:
                print(f"➡️ Invio risposta automatica a: {wa_id}", flush=True)
                send_auto_reply(wa_id)
            else:
                print("⚠️ wa_id mancante nei contatti", flush=True)
        else:
            print("⚠️ Contatti o messaggi mancanti nel payload", flush=True)
    except Exception as e:
        print("❌ Errore nel parsing del messaggio:", str(e), flush=True)

    return jsonify({"status": "received"}), 200

def send_auto_reply(to):
    headers = {
        "Content-Type": "application/json",
        "D360-API-KEY": API_TOKEN
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
    print("📤 Invio messaggio a:", to, flush=True)
    print("🔁 Status:", response.status_code, flush=True)
    print("📨 Response:", response.text, flush=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
