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
        """Alterna el turno, saltando a jugadores muertos si es necesario."""
        if len(self.jugadores) < 2: return
        
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
        
        # Si el siguiente jugador está muerto pero hay alguien vivo en la partida, sigue buscando
        intentos = 0
        while not self.jugadores[self.turno_actual].vivo and intentos < len(self.jugadores):
            self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
            intentos += 1

    def verificar_sobrevivientes(self):
        """Retorna True si al menos un jugador sigue con vida."""
        return any(p.vivo for p in self.jugadores)

    # ------------------------------------------------------------------
    # LOGICA DE JUEGO
    # ------------------------------------------------------------------
    def procesar_movimiento(self, nombre_nodo):
        jugador = self.obtener_jugador_actual()
        if not jugador: return {"Tipo": "Nada"}

        caminos_validos = self.encuentros.rutas_posibles(jugador.nodo_actual)
        if nombre_nodo not in caminos_validos:
            return {"Tipo": "Nada"} 

        jugador.nodo_actual = nombre_nodo
        resultado = self.encuentros.generar_decision(nombre_nodo)
        
        if resultado["Tipo"] == "Muerte":
            jugador.vidas -= 1
            if jugador.vidas <= 0:
                jugador.vivo = False
                # Aquí NO cambiamos de turno, dejamos que el Main detecte 'vivo=False'
        
        elif resultado["Tipo"] == "Premio":
            resultado["SubioNivel"] = jugador.ganar_xp(resultado["Cantidad"])
        
        
        return resultado

    def evolucionar_jugador(self):
        jugador = self.obtener_jugador_actual()
        return self.habilidades.obtener_hijos(jugador.clase, jugador.habilidad_actual)

    # ------------------------------------------------------------------
    # GESTION VISUAL
    # ------------------------------------------------------------------
    def info_visual(self):
        jugador = self.obtener_jugador_actual()
        return self.evolucion.obtener_nombre_evolucion(jugador.clase, jugador.nivel_evolucion)

    def obtener_ruta_imagen_personaje(self):
        jugador = self.obtener_jugador_actual()
        if not jugador: return None
        nombre_evo = self.info_visual()
        return self.rutas.obtener_ruta_personaje(jugador.clase, nombre_evo)

    def obtener_ruta_fondo_nodo(self):
        jugador = self.obtener_jugador_actual()
        nodo = getattr(jugador, "nodo_actual", "Inicio")
        return self.rutas.obtener_ruta_fondo(nodo, es_combate=False)

    def obtener_ruta_fondo_combate(self):
        jugador = self.obtener_jugador_actual()
        nodo = getattr(jugador, "nodo_actual", "Inicio")
        return self.rutas.obtener_ruta_fondo(nodo, es_combate=True)

    def guardar_todo(self):
        return self.datos.guardar_partida(self.jugadores)