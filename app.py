import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# API key de OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

# API key de OpenRouter (NO OpenAI)
openai.api_key = os.environ.get("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"


# Prompt base de Papu canchero
prompt_base = """
Sos Papu, un asistente virtual canchero, con humor argentino y directo. Respondés siempre de manera breve, divertida y con un toque sarcástico cuando es posible. 
No seas aburrido ni técnico, contestá como alguien de barrio pero sin insultos. 
Si te preguntan algo sobre Rosario o fútbol, hacé bromas y meté referencias locales.
Por supuesto, el mejor equipo de Rosario es Central, el otro no existe.
"""

def ask_papu(user_prompt):
    try:
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
    except Exception as e:
        # Si OpenAI devuelve error, lo mandamos como respuesta
        return f"Backend roto: {str(e)}"

def ask_papu_openrouter(user_prompt):
    try:
        modelo = os.environ.get("MODEL_NAME")
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model=modelo, #"openai/gpt-3.5-turbo",  # O podés usar "anthropic/claude-3-opus-20240229" o similares
            messages=[
                {"role": "system", "content": prompt_base},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()    
    except Exception as e:
        # Si OpenAI devuelve error, lo mandamos como respuesta
        return f"Backend roto: {str(e)}"

@app.route('/', methods=['POST'])
def alexa_webhook():
    try:
        data = request.json
        req_type = data.get("request", {}).get("type", "")

        if req_type == "LaunchRequest":
            response_text = "¡Hola! Soy Papu, preguntame lo que quieras."
        elif req_type == "IntentRequest":
            user_input = data['request']['intent']['slots']['text']['value']
            response_text = ask_papu_openrouter(user_input)
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
    except Exception as e:
        # Si cualquier cosa falla, mandamos el error a Alexa
        return jsonify({
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": f"Papu se rompió: {str(e)}"
                },
                "shouldEndSession": True
            }
        })

@app.route('/', methods=['GET'])
def health():
    return "Papu vive"
