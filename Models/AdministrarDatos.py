import json
import os

# Esta clase se encarga de escribir y leer el archivo de guardado
class AdministrarDatos:
    def __init__(self, archivo="datos/sesion_juego.json"):
        self.archivo = archivo
        # Esta linea crea la carpeta 'datos' automaticamente si no existe
        # Evita que el programa explote al intentar guardar
        os.makedirs(os.path.dirname(self.archivo), exist_ok=True)

    def guardar_sesion(self, jugadores, modo, turno):
        """
        Convierte los objetos de los jugadores en un diccionario de texto
        para poder escribirlo en el disco duro.
        """
        data = {
            "config": {"modo": modo, "turno": turno},
            "jugadores": [
                {
                    "id": p.id,
                    "clase": p.clase,
                    "vidas": p.vidas,
                    "hp": p.vida,       # Guarda tus LPs actuales
                    "xp": p.xp,
                    "nivel": p.nivel_evolucion,
                    "hab": p.habilidad_actual,
                    "nodo": p.nodo_actual # Guarda en que parte del mapa te quedaste
                } for p in jugadores
            ]
        }
        try:
            # Abre el archivo y escribe los datos de forma organizada (indent=4)
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            # Si el disco esta lleno o no hay permisos, te avisa aqui
            print(f"Error al escribir JSON: {e}")

    def cargar_sesion(self):
        """
        Busca el archivo guardado y lo traduce de vuelta al juego.
        """
        # Si el archivo no existe, devuelve None para que el juego empiece de cero
        if not os.path.exists(self.archivo):
            return None
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                return json.load(f) # Devuelve la informacion lista para usarse
        except:
            # Si el archivo esta corrupto o vacio, devuelve None
            return None