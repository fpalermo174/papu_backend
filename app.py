import os
import openai
from flask import Flask, request, jsonify
from saludo import saludo_aleatorio
from rosario_central import contiene_pregunta_sobre_central, respuesta_central_random
from logger import guardar_log

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
        guardar_log(f"Modelo usado: {modelo}")
        response = client.chat.completions.create(
            model=modelo, #"openai/gpt-3.5-turbo",  # O podés usar "anthropic/claude-3-opus-20240229" o similares
            messages=[
                {
                    "role": "system", 
                    "content": prompt_base
                },
                {
                    "role": "user", 
                    "content": {
                        "type": "text",
                        "text": user_prompt
                    }
                }],
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
        guardar_log(f"DATA RECIBIDA: {data}")  # <-- línea que graba la request

        req_type = data.get("request", {}).get("type", "")

        if req_type == "LaunchRequest":
            response_text = saludo_aleatorio()
        elif req_type == "IntentRequest":
            intent = data.get("request", {}).get("intent", {})
            slots = intent.get("slots", {})
            user_input = slots.get("text", {}).get("value", "").strip()

            guardar_log(f"TEXTO RECIBIDO: {user_input}")

            if not user_input:
                response_text = "No entendí lo que me dijiste. Probá de nuevo, capo."
            if contiene_pregunta_sobre_central(user_input):
                response_text = respuesta_central_random()
            else:
                response_text = ask_papu_openrouter(user_input)
        else:
            response_text = "No entendí qué me estás pidiendo."

        guardar_log(f"RESPUESTA ENVIADA: {response_text}")

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

@app.route('/logs', methods=['GET'])
def ver_logs():
    try:
        with open("log.txt", encoding="utf-8") as f:
            return f"<pre>{f.read()}</pre>"
    except Exception as e:
        return f"No se pudo leer el log: {e}"
