from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def alexa_webhook():
    data = request.json
    req_type = data.get("request", {}).get("type", "")

    if req_type == "LaunchRequest":
        response_text = "¡Hola! Soy Papu, preguntame lo que quieras."
    elif req_type == "IntentRequest":
        user_input = data['request']['intent']['slots']['text']['value']
        response_text = f"Me dijiste: {user_input}. Todavía no tengo una respuesta inteligente, pero estoy aprendiendo."
    else:
        response_text = "No entendí qué me estás pidiendo."

    return jsonify({
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": response_text
            },
            "shouldEndSession": False
        }
    })

@app.route('/', methods=['GET'])
def health():
    return "Papu vive"
