import pygame
import math

# Clase base que define que es una 'cosa' que puede pelear en el juego
class Entidad:
    def __init__(self, nombre, vida, dano):
        self.nombre = nombre
        self.vida = vida      # Salud actual
        self.dano = dano      # Poder de ataque base

# Esta clase maneja todo lo que hace el usuario (ti, el jugador)
class Player(Entidad):
    def __init__(self, id_player, clase):
        # Llama a Entidad para ponerle nombre 'Jugador', 100 de vida y 10 de daño inicial
        super().__init__(f"Jugador{id_player}", 100, 10)
        self.id = id_player
        self.clase = clase          # Fuego, Agua, Tierra o Aire
        
        # Atributos de supervivencia (Esto es lo que ves en la pantalla de inicio)
        self.vidas = 3              # Tus 3 corazones o intentos globales
        self.vida_max = 100         # El tope de tu barra de LPs
        self.vida = 100             # Los LPs que tienes ahora mismo
        self.vivo = True            # Si esto es False, sale la pantalla de muerte
        
        # Atributos de progreso y mapa
        self.xp = 0                 # Experiencia acumulada
        self.nivel_evolucion = 1    # Nivel actual (Maximo 3)
        self.habilidad_actual = self.obtener_habilidad_inicial()
        self.nodo_actual = "Inicio" # En que parte del mapa estas parado

    def obtener_habilidad_inicial(self):
        # Diccionario que decide tu primer ataque segun el elemento que elegiste
        iniciales = {
            "Fuego": "Chispa", 
            "Agua": "Burbuja", 
            "Tierra": "Terron", 
            "Aire": "Soplido"
        }
        # Si no encuentra la clase, te da un 'Golpe' por defecto
        return iniciales.get(self.clase, "Golpe")

    def ganar_xp(self, cantidad):
        # Esta funcion suma XP y revisa si te toca evolucionar
        self.xp += cantidad
        subio = False
        
        # Si llegas a 100 de XP y no eres nivel maximo, subes de nivel
        if self.xp >= 100 and self.nivel_evolucion < 3:
            self.nivel_evolucion += 1
            self.xp = 0 
            
            # Al evolucionar, el juego te hace mas fuerte automaticamente
            self.dano += 10           # Pegas mas duro
            self.vida_max += 20       # Tu barra de vida crece
            self.vida = self.vida_max # Te cura toda la vida como premio
            
            subio = True
            # Mensaje tecnico para la consola
            print(f"Evolucion! {self.nombre} ahora tiene {self.vida_max} LP y {self.dano} de dano")
        return subio

# Esta clase maneja a los enemigos (Guardias y Boris)
class Enemy(Entidad):
    def __init__(self, nombre, dificultad):
        # Si el nombre es 'Boris', le da el doble de salud que a un enemigo comun
        multiplicador_jefe = 2 if nombre == "Boris" else 1
        
        # Calcula la vida y el daño basandose en el nivel de dificultad del nodo
        hp_base = (50 * dificultad) * multiplicador_jefe
        daño_base = 10 * dificultad
        
        # Le pasa los datos calculados a la clase padre Entidad
        super().__init__(nombre, vida=hp_base, dano=daño_base)
        
        # Guarda el maximo para que la barra roja de salud sepa cuando esta llena
        self.vida_max = hp_base
        self.vida = hp_base
        
        # Marca si es un jefe para que la interfaz pueda poner efectos especiales
        self.es_jefe = (nombre == "Boris")