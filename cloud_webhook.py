from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "events.json"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        event = request.get_json()

        if not event:
            return jsonify({"error": "No JSON received"}), 400

        # Add timestamp (useful later)
        event["received_at"] = datetime.utcnow().isoformat()

        with open(DATA_FILE, "a") as f:
            f.write(json.dumps(event) + "\n")

        print("✅ Event received:", event.get("type"))

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500


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
                continue  # skip bad lines

        return jsonify({"events": events})

    except Exception as e:
        print("❌ Error reading events:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return "Webhook server is running", 200


if __name__ == "__main__":
    app.run(port=5001)
