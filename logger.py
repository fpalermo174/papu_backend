# logger.py
from datetime import datetime

def guardar_log(texto):
    try:
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] {texto}\n")
    except Exception as e:
        # Si algo falla con el log, no queremos que rompa el servidor
        print(f"Error al guardar log: {e}")
