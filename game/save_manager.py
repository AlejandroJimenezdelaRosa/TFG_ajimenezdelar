import json
import os

SAVE_PATH = "savegame.json"

def guardar_partida(partida):
    data = {
        "capitulo": partida.capitulo
    }
    with open(SAVE_PATH, "w") as f:
        json.dump(data, f)

def cargar_partida():
    if not os.path.exists(SAVE_PATH):
        return None

    with open(SAVE_PATH, "r") as f:
        data = json.load(f)

    return data

def hay_partida_guardada():
    return os.path.exists(SAVE_PATH)
