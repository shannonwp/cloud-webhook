from flask import Flask, request
import json
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "8331553657:AAEjB35Mkg6SU0PwglnHIx0sIk3l0xLgfNs"
TELEGRAM_CHAT_ID = "8343076256"


@app.route("/", methods=["GET"])
def home():
    return "OK", 200


@app.route("/stripe-webhook", methods=["POST"])
def stripe_webhook():
    try:
        print("🔥 Webhook hit")

        event = json.loads(request.data)
        event_type = event.get("type", "unknown")

        print("Event:", event_type)

        message = f"💰 Payment event:\n{event_type}"

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        response = requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        })

        print("📲 Telegram response:", response.text)

        return "", 200

    except Exception as e:
        print("❌ Error:", e)
        return "", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
