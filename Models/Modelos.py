import pygame
from Models.Entidades import Player
from Models.SistemaEncuentros import SistemaEncuentros
from Models.AdministrarDatos import AdministrarDatos
from Models.ArbolEvolucion import ArbolEvolucion
from Models.GrafoHabilidades import GrafoHabilidades
from Models.GestorRutas import GestorRutas

# Esta clase es el cerebro del juego. Aqui se une la logica, los datos y las rutas.
class GameModel:
    def __init__(self):
        # Aqui se inicializan todas las herramientas que el juego necesita para funcionar
        self.encuentros = SistemaEncuentros() # El mapa y los eventos
        self.datos = AdministrarDatos()       # El sistema para guardar partida
        self.evolucion = ArbolEvolucion()     # Los nombres de los rangos (titulos)
        self.habilidades = GrafoHabilidades() # El arbol de ataques
        self.rutas = GestorRutas()            # El buscador de archivos de imagen
        
        # Variables de estado del juego
        self.jugadores = []                   # Lista donde guardamos a los protagonistas
        self.turno_actual = 0                 # Indica a quien le toca jugar ahora
        self.modo_juego = 1                   # Define si es 1 jugador o mas

    def agregar_jugador(self, id_player, clase):
        # Crea un nuevo objeto de tipo Player y lo mete en la lista del juego
        nuevo_player = Player(id_player, clase)
        self.jugadores.append(nuevo_player)
    
    def obtener_jugador_actual(self):
        # Funcion de ayuda para saber siempre quien es el jugador que tiene el turno
        if not self.jugadores: return None
        if self.turno_actual >= len(self.jugadores): self.turno_actual = 0
        return self.jugadores[self.turno_actual]

    def cambiar_turno(self):
        """Alterna al siguiente jugador que aun tenga vidas globales."""
        if len(self.jugadores) < 2: return
        
        # Busca el indice del siguiente jugador usando el resto matematico
        siguiente_turno = (self.turno_actual + 1) % len(self.jugadores)
        
        # Si el siguiente jugador tiene 0 vidas, revisa si el actual tambien para no hacer nada
        if self.jugadores[siguiente_turno].vidas <= 0:
            if self.jugadores[self.turno_actual].vidas <= 0:
                return 
        else:
            # Si el siguiente esta vivo, le pasa el turno
            self.turno_actual = siguiente_turno
    
    def verificar_sobrevivientes(self):
        """Revisa si queda algun jugador vivo en la lista para seguir la partida."""
        for p in self.jugadores:
            if p.vidas > 0:
                return True
        return False

    def procesar_movimiento(self, destino):
        """
        Maneja el viaje de un punto a otro en el mapa y procesa que pasa al llegar.
        """
        jugador = self.obtener_jugador_actual()
        if not jugador: return None
        
        # Le pide al sistema de encuentros los caminos que estan conectados
        rutas_validas = self.encuentros.rutas_posibles(jugador.nodo_actual)
        
        # Si el clic fue en un lugar valido, mueve al jugador
        if destino in rutas_validas:
            jugador.nodo_actual = destino
            # Genera que evento hay en ese nuevo lugar (Pelea, Trampa, etc.)
            resultado = self.encuentros.generar_decision(destino)
            
            # Si el evento es una trampa de muerte, quita una vida global
            if resultado["Tipo"] == "Muerte":
                jugador.vidas -= 1
                if jugador.vidas <= 0: 
                    jugador.vivo = False # Si llega a 0, el personaje muere definitivamente
            
            # Si el evento es un premio, le da XP y revisa si sube de nivel
            elif resultado["Tipo"] == "Premio":
                resultado["SubioNivel"] = jugador.ganar_xp(resultado["Cantidad"])
                
            return resultado
        return None

    def evolucionar_jugador(self):
        """Busca en el grafo que ataques nuevos puede aprender el jugador segun su nivel."""
        jugador = self.obtener_jugador_actual()
        if not jugador: return []
        return self.habilidades.obtener_hijos(jugador.clase, jugador.habilidad_actual)

    def info_visual(self):
        """Obtiene el nombre del rango actual (ej: 'Maestro del sol') para mostrarlo en UI."""
        p = self.obtener_jugador_actual()
        if not p: return "Desconocido"
        return self.evolucion.obtener_nombre_evolucion(p.clase, p.nivel_evolucion)

    def obtener_ruta_imagen_personaje(self):
        """Pide al gestor de rutas la imagen que corresponde a la evolucion del jugador."""
        p = self.obtener_jugador_actual()
        if not p: return None
        nombre_evo = self.info_visual()
        return self.rutas.obtener_ruta_personaje(p.clase, nombre_evo)

    def obtener_ruta_fondo_nodo(self):
        """Busca la imagen de fondo del lugar del mapa donde esta parado el jugador."""
        p = self.obtener_jugador_actual()
        nodo = getattr(p, "nodo_actual", "Inicio")
        return self.rutas.obtener_ruta_fondo(nodo, es_combate=False)

    def obtener_ruta_fondo_combate(self):
        """Busca el fondo especial para la pantalla de pelea en ese lugar especifico."""
        p = self.obtener_jugador_actual()
        nodo = getattr(p, "nodo_actual", "Inicio")
        return self.rutas.obtener_ruta_fondo(nodo, es_combate=True)