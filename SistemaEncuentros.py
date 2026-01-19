import random
from Models.Entidades import Enemy

class SistemaEncuentros:
    def __init__(self):
        # El grafo de las rutas define en que lugar del mapa se encuentra el jugador
        self.grafo_mapa = {
            "Inicio": ["Campus", "Comedor"],
            "Campus": ["Ed39", "Piso 5"],
            "Comedor": ["Ed39"],
            "Ed39": ["Piso 5"],
            "Piso 5": [] 
        }

        # eventos define que pasa en cada nodo
        self.eventos = {
            "Campus": "Combate",
            "Ed39": "Trampa",
            "Comedor": "XP_Gratis",
            "Piso 5": "Jefe"
        }
        
    def rutas_posibles(self, nodo_actual):
        #Retorna los caminos que el jugador puede tomar
        return self.grafo_mapa.get(nodo_actual, [])

    #Luego se le agregaran porcentajes a los eventos 
    def generar_decision(self, nodo):
        #Determina que pasa al entrar en un nodo especifico (escenario)
        evento = self.eventos.get(nodo, "Nada")
        
        if evento == "Combate":
            return {"Tipo": "Combate", "Enemigo": Enemy("Guardias", 1)}
            
        elif evento == "Trampa":
            return {"Tipo": "Muerte", "Mensaje": "Te jalaste EDO. Pierdes una vida"}
            
        elif evento == "XP_Gratis":
            return {"Tipo": "Premio", "Cantidad": 50}
            
        elif evento == "Jefe":
            return {"Tipo": "Combate", "Enemigo": Enemy("Boris", 3)}
        
        return {"Tipo": "Seguro"}