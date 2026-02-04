from Models.Entidades import Enemy

# Esta clase define las conexiones entre lugares y los eventos de cada sitio
class SistemaEncuentros:
    def __init__(self):
        # 1. EL GRAFO (El esqueleto del mapa)
        # Define que lugar conecta con cual. Ejemplo: Desde 'Inicio' vas a 'Campus' o 'Comedor'
        self.grafo_mapa = {
            "Inicio": ["Campus", "Comedor"],
            "Campus": ["Ed39", "Piso 5"],
            "Comedor": ["Ed39"],
            "Ed39": ["Piso 5"],
            "Piso 5": [] # Ultimo nivel, no tiene mas salidas
        }
        
        # 2. LOS EVENTOS (Que hay en cada sitio)
        self.eventos = {
            "Campus": "Combate",
            "Ed39": "Trampa",
            "Comedor": "XP_Gratis",
            "Piso 5": "Jefe" # Aqui es donde aparece Boris
        }

    def rutas_posibles(self, nodo_actual):
        """
        Calcula a que lugares puedes saltar desde donde estas parado.
        Busca tanto caminos hacia adelante como hacia atras.
        """
        adyacentes = []
        # Agrega los destinos directos desde el nodo actual
        if nodo_actual in self.grafo_mapa:
            adyacentes.extend(self.grafo_mapa[nodo_actual])
            
        # Agrega los lugares que tienen al nodo actual como destino (para poder volver)
        for origen, destinos in self.grafo_mapa.items():
            if nodo_actual in destinos:
                adyacentes.append(origen)
        
        # list(set(...)) elimina duplicados por si acaso
        return list(set(adyacentes))

    def generar_decision(self, nodo):
        """
        Esta es la funcion mas importante. Decide que le pasa al jugador al entrar a un nodo.
        """
        evento = self.eventos.get(nodo, "Nada")
        
        # Si el evento es pelea o el jefe final
        if evento == "Combate" or evento == "Jefe":
            # Si es el jefe (Piso 5), la dificultad sube a 3
            dif = 3 if evento == "Jefe" else 1
            return {"Tipo": "Combate", "Enemigo": Enemy("Guardia", dif)}
        
        # Evento de muerte instantanea (La famosa trampa de EDO)
        elif evento == "Trampa":
            return {"Tipo": "Muerte", "Mensaje": "¡TE JALASTE EDO! El examen fue superior a ti."}
        
        # Evento de ayuda (XP gratis)
        elif evento == "XP_Gratis":
            return {"Tipo": "Premio", "Cantidad": 50}
            
        # Si el nodo no tiene evento, no pasa nada
        return {"Tipo": "Nada"}