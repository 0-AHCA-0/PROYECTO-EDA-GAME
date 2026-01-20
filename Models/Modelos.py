#Esta clase va a actuar como un tipo de controlador de todos los modelos
#Sigue siendo un modelo (Esta clase se tiene que usar para el desarrollo del juego, NO LAS OTRAS)

#Importamos todos los modelos

from Models.Entidades import Player
from Models.SistemaEncuentros import SistemaEncuentros
from Models.AdministrarDatos import AdministrarDatos
from Models.ArbolEvolucion import ArbolEvolucion
from Models.GrafoHabilidades import GrafoHabilidades

class GameModel:
    def __init__(self):
        self.encuentros = SistemaEncuentros()
        self.datos = AdministrarDatos()
        self.evolucion = ArbolEvolucion()
        self.habilidades = GrafoHabilidades()
        self.jugadores = []
        self.turno_actual = 0
    
    def agregar_jugador(self, id_player, clase):
        nuevo_player = Player(id_player, clase)
        self.jugadores.append(nuevo_player)
    
    def obtener_jugador_actual(self):
        """Método único para obtener el jugador del turno"""
        if self.jugadores:
            return self.jugadores[self.turno_actual]
        return None
    
    #Metodo para saber la clase y la habilidad del jugador
    def evolucionar_jugador(self):
        jugador = self.obtener_jugador_actual()
        return self.habilidades.obtener_hijos(jugador.clase, jugador.habilidad_actual)
    
    def info_visual(self):
        jugador = self.obtener_jugador_actual()
        # Usamos el método de la clase evolución para mantener el orden
        return self.evolucion.obtener_nombre_evolucion(jugador.clase, jugador.nivel_evolucion)
    
    #Funcion de turno actual
    def cambiar_turno(self):
        self.turno_actual = 1 if self.turno_actual == 0 else 0
    
    def procesar_movimiento(self, nombre_nodo):
        """
        1. Encontramos al jugador actual, junto al nodo en el que se encuentra. 
        2. Luego de eso si se cae en Muerte se le resta al jugador 1 vida y pasa al otro jugador 
        3. si cae en un cofre se le aumenta la experiencia
        
        """
        jugador = self.obtener_jugador_actual()
        jugador.nodo_actual = nombre_nodo
        
        resultado = self.encuentros.generar_decision(nombre_nodo)
        
        if resultado["Tipo"] == "Muerte":
            jugador.vidas -= 1
            if jugador.vidas <= 0:
                jugador.vivo = False
            # El turno cambia al final de la función para todos los casos
            
        elif resultado["Tipo"] == "Premio":
            # Si subio_nivel es True, guardamos para activar animación en el Main
            resultado["SubioNivel"] = jugador.ganar_xp(resultado["Cantidad"])
        
        self.cambiar_turno()
        return resultado 

    #Guardamos la partida
    def guardar_todo(self):
        return self.datos.guardar_partida(self.jugadores)
    