import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

WHATSAPP_API_URL = "https://waba-v2.360dialog.io/messages"
API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")  # Impostata in Render env

@app.route("/", methods=["GET"])
def health():
    return "Webhook OK", 200

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    print("Ricevuto messaggio:", data)

    try:
        # Estrai il numero del mittente (wa_id)
        contacts = data.get("contacts", [])
        messages = data.get("messages", [])
        if contacts and messages:
            wa_id = contacts[0].get("wa_id")
            if wa_id:
                print(f"Invio risposta automatica a: {wa_id}")
                send_auto_reply(wa_id)
            else:
                print("wa_id mancante nei contatti")
        else:
            print("Contatti o messaggi mancanti nel payload")
    except Exception as e:
        print("Errore nel parsing del messaggio:", str(e))

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
    print("Invio messaggio a:", to)
    print("Status:", response.status_code)
    print("Response:", response.text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
