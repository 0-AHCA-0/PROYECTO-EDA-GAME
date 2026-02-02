class Entidad:
    def __init__(self, nombre, vida, dano):
        self.nombre = nombre
        self.vida = vida
        self.dano = dano

class Player(Entidad):
    def __init__(self, id_player, clase):
        # IMPORTANTE: Aquí pasamos vida=100 y dano=10 al constructor de Entidad
        super().__init__(f"Jugador{id_player}", 100, 10)
        self.id = id_player
        self.clase = clase
        self.vidas = 5
        self.xp = 0
        self.nivel_evolucion = 1
        self.habilidad_actual = self.obtener_habilidad_inicial()
        self.vivo = True
        self.nodo_actual = "Inicio"

    def obtener_habilidad_inicial(self):
        iniciales = {"Fuego": "Chispa", "Agua": "Burbuja", "Tierra": "Terron", "Aire": "Soplido"}
        return iniciales.get(self.clase, "Desconocido")

    def ganar_xp(self, cantidad):
        self.xp += cantidad
        subio = False
        
        if self.xp >= 100 and self.nivel_evolucion < 3:
            self.nivel_evolucion += 1
            self.xp = 0 
            
            # --- MEJORA DE ATAQUE ---
            # Cada vez que evoluciona, el daño base sube 10 puntos
            self.dano += 10 
            
            subio = True
            print(f"¡{self.nombre} evolucionó! Ahora su daño es: {self.dano}")
        return subio

class Enemy(Entidad):
    def __init__(self, nombre, dificultad):
        # El enemigo escala su vida según la dificultad
        super().__init__(nombre, vida=50 * dificultad, dano=1)