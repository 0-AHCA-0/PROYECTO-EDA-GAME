#Clase que definira las habilidades iniciales y sus respectivas mejoras dependiendo del tipo elegido
class GrafoHabilidades:
    def __init__(self):
        #Hacemos un diccionario con el tipo de carta seleccionado y las habilidades con sus respectivas variantes para elegir
        #Cada una cuaenta con su grafo. Por el momento solo hay esas.
        #Se agregaran mas habilidades en el futuro.
        self.grafos = {
            "Fuego": {
                "Chispa": ["Bola de Fuego", "Enviste Igneo"],
                "Bola de Fuego": ["Inferno"],
                "Enviste Igneo": ["Explosion Solar"],
                "Explosion Solar": [],
                "Inferno": []
            },
            "Agua": {
                "Burbuja": ["Squirt", "Sana Sana"],
                "Squirt": ["Tsunami"],
                "Sana Sana": ["Sana Colita de Rana"],
                "Tsunami": [],
                "Sana Colita de Rana": []
            },
            "Tierra": {
                "Terron": ["KKCK", "Lodo"],
                "KKCK": ["Churreta"],
                "Lodo": ["Pantano"],
                "Churreta": [],
                "Pantano": []
            },
            "Aire": {
                "Soplido": ["Afixia", "Levitar"],
                "Afixia": ["Chupa Almas"],
                "Levitar": ["Patada Voladora"],
                "Chupa Almas": [],
                "Patada Voladora": []
            }
        }
    
    def obtener_hijos(self, clase, habilidad_actual):
        """Retorna la lista de habilidades siguientes en el grafo"""
        return self.grafos.get(clase, {}).get(habilidad_actual, [])
