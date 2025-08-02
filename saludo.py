import random

def saludo_aleatorio():
    with open("saludos.txt", encoding="utf-8") as f:
        saludos = f.readlines()
    return random.choice(saludos).strip()
