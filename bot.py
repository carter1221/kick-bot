import requests
import time
import json
import os

# ====== CONFIGURACIÓN ======
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")       # variable de entorno
KICK_CHANNEL = os.getenv("KICK_CHANNEL")           # variable de entorno
DB_FILE = "usuarios.json"
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))

# ====== FUNCIONES TELEGRAM ======
def cargar_usuarios():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def guardar_usuarios(usuarios):
    with open(DB_FILE, "w") as f:
        json.dump(usuarios, f)

def get_updates():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    r = requests.get(url).json()
    return r.get("result", [])

def registrar_usuarios():
    usuarios = cargar_usuarios()
    updates = get_updates()
    for update in updates:
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            if text == "/start" and chat_id not in usuarios:
                usuarios.append(chat_id)
                print(f"Nuevo usuario registrado: {chat_id}")
                send_message(chat_id, "✅ Te has suscrito a los avisos de directos en Kick.")
    guardar_usuarios(usuarios)

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})

def broadcast(text):
    usuarios = cargar_usuarios()
    for uid in usuarios:
        send_message(uid, text)

# ====== FUNCIONES KICK ======
def is_live_kick():
    url = f"https://kick.com/api/v2/channels/{KICK_CHANNEL}"
    response = requests.get(url).json()
    return response.get("livestream") is not None

# ====== LOOP PRINCIPAL ======
if __name__ == "__main__":
    was_live = False

    while True:
        try:
            registrar_usuarios()

            live = is_live_kick()

            if live and not was_live:
                broadcast(f"🟢 ¡{KICK_CHANNEL} está EN DIRECTO en Kick! 👉 https://kick.com/{KICK_CHANNEL}")
                broadcast("🟢 Test: El bot está funcionando correctamente.")


            was_live = live

        except Exception as e:
            print("Error:", e)

        time.sleep(CHECK_INTERVAL)

