@app.route("/stripe-webhook", methods=["POST"])
def stripe_webhook():
    try:
        print("🔥 Webhook hit")

        # Use raw data (Stripe-safe)
        payload = request.data
        print("Payload received")

        event = json.loads(payload)

        event["received_at"] = datetime.utcnow().isoformat()

        with open(DATA_FILE, "a") as f:
            f.write(json.dumps(event) + "\n")

        print("✅ Event received:", event.get("type"))

        return "", 200

    except Exception as e:
        print("❌ Error:", e)
        return "", 500
