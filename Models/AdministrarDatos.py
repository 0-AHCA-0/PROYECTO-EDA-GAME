import json
import os

class AdministrarDatos:
    def __init__(self, archivo="datos/sesion_juego.json"):
        self.archivo = archivo
        # Asegura que la carpeta exista
        os.makedirs(os.path.dirname(self.archivo), exist_ok=True)

    def guardar_sesion(self, jugadores, modo, turno):
        data = {
            "config": {"modo": modo, "turno": turno},
            "jugadores": [
                {
                    "id": p.id,
                    "clase": p.clase,
                    "vidas": p.vidas,
                    "hp": p.vida,
                    "xp": p.xp,
                    "nivel": p.nivel_evolucion,
                    "hab": p.habilidad_actual,
                    "nodo": p.nodo_actual
                } for p in jugadores
            ]
        }
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error al escribir JSON: {e}")

    def cargar_sesion(self):
        if not os.path.exists(self.archivo):
            return None
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None