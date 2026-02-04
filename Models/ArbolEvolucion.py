import pygame

# Esta clase guarda todos los titulos y nombres de las evoluciones
class ArbolEvolucion:
    def __init__(self):
        # Diccionario principal: Organizado por Elemento -> Nivel
        # Se usa str(nivel) porque las llaves "1", "2" y "3" son texto
        self.evoluciones = {
            "Fuego": {
                "1": "Aprendiz Hot", 
                "2": "Experto en Fuego", 
                "3": "Maestro del sol"
            },
            "Agua": {
                "1": "Gota Joven", 
                "2": "Laguna del Sabio", 
                "3": "Espiritu del Oceano"
            },
            "Tierra": {
                "1": "Semilla", 
                "2": "Mugre", 
                "3": "Duro como una Piedra"
            },
            "Aire": {
                "1": "Brisa", 
                "2": "Pies ligeros", 
                "3": "Huracan Viviente"
            },
        }
    
    def obtener_nombre_evolucion(self, clase, nivel):
        """
        Esta funcion busca en el diccionario el nombre que corresponde.
        Sirve para que la interfaz sepa que texto poner sobre la carta del jugador.
        """

        return self.evoluciones.get(clase, {}).get(str(nivel), "Desconocido")