import pygame
from Models.Entidades import Player
from Models.SistemaEncuentros import SistemaEncuentros
from Models.AdministrarDatos import AdministrarDatos
from Models.ArbolEvolucion import ArbolEvolucion
from Models.GrafoHabilidades import GrafoHabilidades
from Models.GestorRutas import GestorRutas

class GameModel:
    def __init__(self):
        self.encuentros = SistemaEncuentros()
        self.datos = AdministrarDatos()
        self.evolucion = ArbolEvolucion()
        self.habilidades = GrafoHabilidades()
        self.rutas = GestorRutas() 
        
        self.jugadores = []
        self.turno_actual = 0
        self.modo_juego = 1 

    # ------------------------------------------------------------------
    # GESTION DE JUGADORES Y TURNOS
    # ------------------------------------------------------------------
    def agregar_jugador(self, id_player, clase):
        nuevo_player = Player(id_player, clase)
        self.jugadores.append(nuevo_player)
    
    def obtener_jugador_actual(self):
        if not self.jugadores: return None
        if self.turno_actual >= len(self.jugadores): self.turno_actual = 0
        return self.jugadores[self.turno_actual]

    def cambiar_turno(self):
        """Alterna el turno en modo 2P."""
        if len(self.jugadores) < 2: return
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
    
    def verificar_sobrevivientes(self):
        """Revisa si al menos un jugador sigue con vidas disponibles."""
        for p in self.jugadores:
            if p.vidas > 0:
                return True
        return False

    # ------------------------------------------------------------------
    # LÓGICA DE MOVIMIENTO Y ENCUENTROS
    # ------------------------------------------------------------------
    def procesar_movimiento(self, destino):
        jugador = self.obtener_jugador_actual()
        if not jugador: return None
        
        rutas_validas = self.encuentros.rutas_posibles(jugador.nodo_actual)
        
        if destino in rutas_validas:
            jugador.nodo_actual = destino
            # Generar evento (Combate, Trampa, XP, etc.)
            resultado = self.encuentros.generar_decision(destino)
            
            # Procesar consecuencias inmediatas
            if resultado["Tipo"] == "Muerte":
                jugador.vidas -= 1
                if jugador.vidas <= 0: 
                    jugador.vivo = False
            elif resultado["Tipo"] == "Premio":
                resultado["SubioNivel"] = jugador.ganar_xp(resultado["Cantidad"])
                
            return resultado
        return None

    def evolucionar_jugador(self):
        """Retorna las opciones de habilidades hijas según el grafo."""
        jugador = self.obtener_jugador_actual()
        if not jugador: return []
        return self.habilidades.obtener_hijos(jugador.clase, jugador.habilidad_actual)

    # ------------------------------------------------------------------
    # HELPERS VISUALES (Sincronización con Vistas)
    # ------------------------------------------------------------------
    def info_visual(self):
        """Retorna el nombre del rango de evolución (ej: 'Aprendiz Hot')."""
        p = self.obtener_jugador_actual()
        if not p: return "Desconocido"
        return self.evolucion.obtener_nombre_evolucion(p.clase, p.nivel_evolucion)

    def obtener_ruta_imagen_personaje(self):
        """Busca la imagen dinámica del personaje según su evolución."""
        p = self.obtener_jugador_actual()
        if not p: return None
        nombre_evo = self.info_visual()
        return self.rutas.obtener_ruta_personaje(p.clase, nombre_evo)

    def obtener_ruta_fondo_nodo(self):
        """Obtiene el fondo del mapa según el nodo actual."""
        p = self.obtener_jugador_actual()
        nodo = getattr(p, "nodo_actual", "Inicio")
        return self.rutas.obtener_ruta_fondo(nodo, es_combate=False)

    def obtener_ruta_fondo_combate(self):
        """Obtiene el fondo específico para la pantalla de combate."""
        p = self.obtener_jugador_actual()
        nodo = getattr(p, "nodo_actual", "Inicio")
        return self.rutas.obtener_ruta_fondo(nodo, es_combate=True)