from Models.Entidades import Enemy

class SistemaEncuentros:
    def __init__(self):
        # 1. DEFINICION DEL MAPA (GRAFO)
        # Establece que nodos estan conectados con cuales de forma unidireccional
        self.grafo_mapa = {
            "Inicio": ["Campus", "Comedor"],
            "Campus": ["Ed39", "Piso 5"],
            "Comedor": ["Ed39"],
            "Ed39": ["Piso 5"],
            "Piso 5": [] # Nodo final, no tiene mas salidas
        }

        # 2. TABLA DE EVENTOS
        # Asigna que tipo de situacion ocurre en cada nodo del mapa
        self.eventos = {
            "Campus": "Combate",
            "Ed39": "Trampa",
            "Comedor": "XP_Gratis",
            "Piso 5": "Jefe" 
        }

    def rutas_posibles(self, nodo_actual):
        """
        Calcula los movimientos validos desde la posicion actual.
        Permite avanzar segun el grafo y tambien retroceder a nodos previos.
        """
        adyacentes = []
        
        # Agrega destinos permitidos (Hacia adelante)
        if nodo_actual in self.grafo_mapa:
            adyacentes.extend(self.grafo_mapa[nodo_actual])
            
        # Agrega origenes que conectan aqui (Hacia atras)
        for origen, destinos in self.grafo_mapa.items():
            if nodo_actual in destinos:
                adyacentes.append(origen)
                
        # Retorna la lista sin duplicados usando set
        return list(set(adyacentes))

    def generar_decision(self, nodo):
        """
        El corazon de la narrativa. Decide que sucede y que textos se muestran.
        Centraliza todos los mensajes de derrota para que el controlador no invente nada.
        """
        evento = self.eventos.get(nodo, "Nada")
        
        # CASO A: SITUACIONES DE PELEA (Guardias o Jefe Final)
        if evento == "Combate" or evento == "Jefe":
            # Ajuste de dificultad y nombre segun el tipo de pelea
            dif = 3 if evento == "Jefe" else 1
            nombre_e = "Boris" if evento == "Jefe" else "Guardia"
            
            # Configuracion de textos para la pantalla de muerte en combate
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
        
        # CASO B: MUERTE INSTANTANEA (Trampas academicas)
        elif evento == "Trampa":
            return {
                "Tipo": "Muerte", 
                "Titulo": "FALLO ACADEMICO",
                "Mensaje": "TE JALASTE EDO. EL EXAMEN FUE SUPERIOR A TI..."
            }
        
        # CASO C: BENEFICIOS (XP Directa)
        elif evento == "XP_Gratis":
            return {"Tipo": "Premio", "Cantidad": 50}
            
        # CASO D: NODO VACIO
        return {"Tipo": "Nada"}