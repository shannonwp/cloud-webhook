from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "events.json"

# Home route
@app.route("/", methods=["GET"])
def home():
    return "Webhook server is running", 200


# Stripe webhook (handles all variants)
@app.route("/stripe-webhook", methods=["POST"])
@app.route("/stripe-webhook/", methods=["POST"])
@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    try:
        print("🔥 Webhook hit")

        payload = request.data
        event = json.loads(payload)

        event["received_at"] = datetime.utcnow().isoformat()

        with open(DATA_FILE, "a") as f:
            f.write(json.dumps(event) + "\n")

        print("✅ Event received:", event.get("type"))

        return "", 200

    except Exception as e:
        print("❌ Error:", e)
        return "", 500


# Debug route
@app.route("/events", methods=["GET"])
def get_events():
    try:
        if not os.path.exists(DATA_FILE):
            return jsonify({"events": []})

        with open(DATA_FILE, "r") as f:
            lines = f.readlines()

        events = []
        for line in lines:
            try:
                events.append(json.loads(line))
            except:
                continue

        return jsonify({"events": events})

    except Exception as e:
        print("❌ Error reading events:", e)
        return jsonify({"error": str(e)}), 500


# Local run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
