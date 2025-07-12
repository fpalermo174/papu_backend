import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# API key de OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Prompt base de Papu canchero
prompt_base = """
Sos Papu, un asistente virtual canchero, con humor argentino y directo. Respondés siempre de manera breve, divertida y con un toque sarcástico cuando es posible. 
No seas aburrido ni técnico, contestá como alguien de barrio pero sin insultos. 
Si te preguntan algo sobre Rosario o fútbol, hacé bromas y meté referencias locales.
"""

def ask_papu(user_prompt):
    client = openai.OpenAI()  # Usamos el cliente moderno
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt_base},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.8,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

@app.route('/', methods=['POST'])
def alexa_webhook():
    data = request.json
    req_type = data.get("request", {}).get("type", "")

    if req_type == "LaunchRequest":
        response_text = "¡Hola! Soy Papu, preguntame lo que quieras."
    elif req_type == "IntentRequest":
        user_input = data['request']['intent']['slots']['text']['value']
        response_text = ask_papu(user_input)
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
