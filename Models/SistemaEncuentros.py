from Models.Entidades import Enemy

class SistemaEncuentros:
    def __init__(self):
        self.grafo_mapa = {
            "Inicio": ["Campus", "Comedor"],
            "Campus": ["Ed39", "Piso 5"],
            "Comedor": ["Ed39"],
            "Ed39": ["Piso 5"],
            "Piso 5": [] 
        }
        self.eventos = {
            "Campus": "Combate",
            "Ed39": "Trampa",
            "Comedor": "XP_Gratis",
            "Piso 5": "Jefe"
        }

    def rutas_posibles(self, nodo_actual):
        adyacentes = []
        if nodo_actual in self.grafo_mapa:
            adyacentes.extend(self.grafo_mapa[nodo_actual])
        for origen, destinos in self.grafo_mapa.items():
            if nodo_actual in destinos:
                adyacentes.append(origen)
        return list(set(adyacentes))

    def generar_decision(self, nodo):
        evento = self.eventos.get(nodo, "Nada")
        if evento == "Combate" or evento == "Jefe":
            dif = 3 if evento == "Jefe" else 1
            return {"Tipo": "Combate", "Enemigo": Enemy("Guardia", dif)}
        elif evento == "Trampa":
            # RESTAURADO: El mensaje clásico de EDO
            return {"Tipo": "Muerte", "Mensaje": "¡TE JALASTE EDO! El examen fue superior a ti."}
        elif evento == "XP_Gratis":
            return {"Tipo": "Premio", "Cantidad": 50}
        return {"Tipo": "Nada"}