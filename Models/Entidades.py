class Entidad:
    def __init__(self, nombre, vida, dano):
        self.nombre = nombre
        self.vida = vida
        self.dano = dano

class Player(Entidad):
    def __init__(self, id_player, clase):
        super().__init__(f"Jugador{id_player}", 100, 10)
        self.id = id_player
        self.clase = clase
        
        # Atributos de supervivencia
        self.vidas = 3              # Vidas globales (corazones)
        self.vida_max = 100         # LPs máximos
        self.vida = 100             # LPs actuales
        self.vivo = True            # <--- CRÍTICO
        
        # Atributos de progreso
        self.xp = 0
        self.nivel_evolucion = 1
        self.habilidad_actual = self.obtener_habilidad_inicial()
        self.nodo_actual = "Inicio"

    def obtener_habilidad_inicial(self):
        """Asigna el primer ataque según la clase elegida."""
        iniciales = {
            "Fuego": "Chispa", 
            "Agua": "Burbuja", 
            "Tierra": "Terron", 
            "Aire": "Soplido"
        }
        return iniciales.get(self.clase, "Golpe")

    def ganar_xp(self, cantidad):
        """Gestiona la experiencia y la evolución de estadísticas."""
        self.xp += cantidad
        subio = False
        if self.xp >= 100 and self.nivel_evolucion < 3:
            self.nivel_evolucion += 1
            self.xp = 0 
            
            # Escalado de estadísticas al evolucionar
            self.dano += 10 
            self.vida_max += 20     # Aumenta el tope de la barra de vida
            self.vida = self.vida_max # Cura al jugador completamente
            
            subio = True
            print(f"¡Evolución! {self.nombre} ahora tiene {self.vida_max} LP y {self.dano} de daño")
        return subio

class Enemy(Entidad):
    def __init__(self, nombre, dificultad):
        # El enemigo escala vida y daño según la dificultad del nodo
        super().__init__(nombre, vida=50 * dificultad, dano=15 * dificultad)
        self.vidas_max = self.vida # Necesario para que la barra de vida de la vista funcione