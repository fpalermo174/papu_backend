from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def alexa_webhook():
    data = request.json
    print("Recibido:", data)

    # Extraemos lo que dice el usuario
    user_input = data.get('request', {}).get('intent', {}).get('slots', {}).get('text', {}).get('value', 'Nada recibido')

    # Respuesta de prueba
    response_text = f"Me dijiste: {user_input}. Aún no estoy muy listo."

    return jsonify({
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": response_text
            },
            "shouldEndSession": True
        }
    })

@app.route('/', methods=['GET'])
def health_check():
    return "Papu está vivo 🚀"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
