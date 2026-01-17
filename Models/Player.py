
class Player:
    def __init__(self, id_player, clase):
        self.id = id_player
        self.clase = clase
        self.vidas = 3
        self.xp = 0
        self.nivel_evolucion = 1
        self.habilidad_actual = self.obtener_habilidad_inicial()
        self.vivo = True
        
    def _obtener_habilidad_inicial(self):
        iniciales = {"Fuego": "Chispa", "Agua": "Burbuja", "Tierra": "Terron", "Aire": "Soplido"}
        return iniciales.get(self.clase, "Desconocido")
    
    def _ganar_xp(self, cantidad):
        self.xp += cantidad
        if self.xp >= 100 and self.nivel_evolucion < 3:
            self.nivel_evolucion = 3
            return True
        return False