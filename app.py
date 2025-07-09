import os
import sys
import requests
from flask import Flask, request, jsonify

# Per log immediati su Render
sys.stdout.reconfigure(line_buffering=True)

app = Flask(__name__)

# URL API WhatsApp 360dialog
WHATSAPP_API_URL = "https://waba-v2.360dialog.io/messages"
API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")

@app.route("/", methods=["GET"])
def health():
    return "Webhook OK", 200

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    print("📥 Ricevuto messaggio:", data, flush=True)

    try:
        # Naviga correttamente la struttura di 360dialog
        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})

        messages = value.get("messages", [])
        contacts = value.get("contacts", [])

        if messages:
            if contacts:
                wa_id = contacts[0].get("wa_id")
            else:
                wa_id = messages[0].get("from")

            if wa_id:
                print(f"➡️ Invio template a: {wa_id}", flush=True)
                send_auto_reply(wa_id)
            else:
                print("⚠️ Impossibile determinare wa_id", flush=True)
        else:
            print("⚠️ Nessun messaggio ricevuto", flush=True)
    except Exception as e:
        print("❌ Errore durante la gestione del messaggio:", str(e), flush=True)

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
            "name": "risposta_automatica",  # Sostituisci con il nome esatto del tuo template
            "language": {
                "code": "it"  # Codice lingua approvato per il template
            }
        }
    }

    response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)

    print("📤 Messaggio inviato a:", to, flush=True)
    print("🔁 Status:", response.status_code, flush=True)
    print("📨 Response:", response.text, flush=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
