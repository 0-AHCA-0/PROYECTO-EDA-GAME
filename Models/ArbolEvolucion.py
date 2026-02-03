
#Clase con diccionarios que contienen el arbol de evolucion.
#En el futuro de agregara mas 
class ArbolEvolucion:
    def __init__(self):
        self.evoluciones = {
            "Fuego":{"1": "Aprendiz Hot","2": "Experto en Fuego","3": "Maestro del sol"},
            "Agua":{"1": "Gota Joven","2": "Laguna del Sabio","3": "Espiritu del Oceano"},
            "Tierra":{"1": "Semilla","2": "Mugre","3": "Duro como una Piedra"},
            "Aire":{"1": "Brisa","2": "Pies ligeros","3": "Huracan Viviente"},
        }
    
    def obtener_nombre_evolucion(self, clase, nivel):
        """Retorna el nombre según la clase y nivel (1, 2 o 3)"""
        return self.evoluciones.get(clase, {}).get(str(nivel), "Desconocido")