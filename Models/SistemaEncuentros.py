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
        """
        Toda la informacion de texto sale de aqui. 
        Si se quiere cambiar un mensaje, ae hace solo aqui.
        """
        evento = self.eventos.get(nodo, "Nada")
        
        if evento == "Combate" or evento == "Jefe":
            dif = 3 if evento == "Jefe" else 1
            nombre_e = "Boris" if evento == "Jefe" else "Guardia"
            
            # Definimos los textos especificos para el combate
            if evento == "Jefe":
                titulo_m = "PROYECTO RECHAZADO"
                msg_m = "TE JALASTE EDA. BORIS NO ACEPTO TU PROYECTO PUCE."
            else:
                titulo_m = "TE QUITARON LA MARIA"
                msg_m = "UN GUARDIA TE HA ATRAPADO. TE JALASTE EDA POR FUMAR MARIA."
            
            return {
                "Tipo": "Combate", 
                "Enemigo": Enemy(nombre_e, dif),
                "TituloMuerte": titulo_m,
                "Mensaje": msg_m
            }
        
        elif evento == "Trampa":
            return {
                "Tipo": "Muerte", 
                "Titulo": "FALLO ACADEMICO",
                "Mensaje": "TE JALASTE EDO. EL EXAMEN FUE SUPERIOR A TI..."
            }
        
        elif evento == "XP_Gratis":
            return {"Tipo": "Premio", "Cantidad": 50}
            
        return {"Tipo": "Nada"}