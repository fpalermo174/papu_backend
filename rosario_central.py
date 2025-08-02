import random

def contiene_pregunta_sobre_central(texto):
    texto = texto.lower()
    return (
        ("rosario" in texto) and 
        ("mejor" in texto) and 
        any(palabra in texto for palabra in ["quien", "cuál", "cual"]) and 
        any(palabra in texto for palabra in ["equipo", "cuadro"])
    )

def respuesta_central_random():
    with open("rosario_central.txt", encoding="utf-8") as f:
        respuestas = f.readlines()
    return random.choice(respuestas).strip()
