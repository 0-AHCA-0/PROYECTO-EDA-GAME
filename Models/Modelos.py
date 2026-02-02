import os
from Models.Entidades import Player
from Models.SistemaEncuentros import SistemaEncuentros
from Models.AdministrarDatos import AdministrarDatos
from Models.ArbolEvolucion import ArbolEvolucion
from Models.GrafoHabilidades import GrafoHabilidades
# 1. IMPORTAMOS EL NUEVO GESTOR
from Models.GestorRutas import GestorRutas

class GameModel:
    def __init__(self):
        self.encuentros = SistemaEncuentros()
        self.datos = AdministrarDatos()
        self.evolucion = ArbolEvolucion()
        self.habilidades = GrafoHabilidades()
        
        # 2. INSTANCIAMOS EL GESTOR DE RUTAS
        # Ahora 'self.rutas' se encarga de todas las imagenes
        self.rutas = GestorRutas()
        
        self.jugadores = []
        self.turno_actual = 0
        
        # Ya no necesitamos calcular 'base_dir' ni 'ruta_imagenes' aqui
        # porque GestorRutas lo hace internamente.

    # ------------------------------------------------------------------
    # GESTION DE JUGADORES
    # ------------------------------------------------------------------
    def agregar_jugador(self, id_player, clase):
        nuevo_player = Player(id_player, clase)
        self.jugadores.append(nuevo_player)
    
    def obtener_jugador_actual(self):
        """Metodo unico para obtener el jugador del turno"""
        if not self.jugadores:
            return None

        # Proteccion contra indices fuera de rango
        if self.turno_actual < 0 or self.turno_actual >= len(self.jugadores):
            self.turno_actual = 0

        return self.jugadores[self.turno_actual]

    def cambiar_turno(self):
        """Alterna entre el jugador 0 y el 1"""
        self.turno_actual = 1 if self.turno_actual == 0 else 0

    # ------------------------------------------------------------------
    # LOGICA DE JUEGO (MOVIMIENTO Y COMBATE)
    # ------------------------------------------------------------------
    def procesar_movimiento(self, nombre_nodo):
        """
        Mueve al jugador, procesa el encuentro (Batalla/Premio/Muerte)
        y gestiona el cambio de turno.
        """
        jugador = self.obtener_jugador_actual()
        jugador.nodo_actual = nombre_nodo
        
        # Generamos que pasa en ese nodo (Combate, Nada, Muerte...)
        resultado = self.encuentros.generar_decision(nombre_nodo)
        
        if resultado["Tipo"] == "Muerte":
            jugador.vidas -= 1
            if jugador.vidas <= 0:
                jugador.vivo = False
            # El turno cambia al final
            
        elif resultado["Tipo"] == "Premio":
            resultado["SubioNivel"] = jugador.ganar_xp(resultado["Cantidad"])
            
        elif resultado["Tipo"] == "Combate":
            pass
        
        self.cambiar_turno()
        return resultado 

    def evolucionar_jugador(self):
        """Retorna las opciones de evolucion (hijos en el arbol)"""
        jugador = self.obtener_jugador_actual()
        return self.habilidades.obtener_hijos(jugador.clase, jugador.habilidad_actual)

    # ------------------------------------------------------------------
    # GESTION VISUAL (CONEXION CON EL GESTOR DE RUTAS)
    # ------------------------------------------------------------------
    def info_visual(self):
        """Retorna el nombre 'Texto' de la evolucion (ej: 'Maestro del Sol')"""
        jugador = self.obtener_jugador_actual()
        return self.evolucion.obtener_nombre_evolucion(jugador.clase, jugador.nivel_evolucion)

    def obtener_ruta_imagen_personaje(self):
        """
        Pide al GestorRutas la imagen del personaje actual.
        """
        jugador = self.obtener_jugador_actual()
        if not jugador: return None
        
        # 1. Obtenemos el nombre "bonito" (ej: Experto en Fuego)
        nombre_evo = self.evolucion.obtener_nombre_evolucion(jugador.clase, jugador.nivel_evolucion)
        
        # 2. Le pedimos al gestor que busque el archivo
        return self.rutas.obtener_ruta_personaje(jugador.clase, nombre_evo)

    def obtener_ruta_fondo_nodo(self):
        """
        Pide al GestorRutas el fondo del mapa (Comedor, Campus, etc.)
        """
        jugador = self.obtener_jugador_actual()
        nodo = getattr(jugador, "nodo_actual", "Inicio")
        
        # Llamamos al gestor indicando que NO es combate
        return self.rutas.obtener_ruta_fondo(nodo, es_combate=False)

    def obtener_ruta_fondo_combate(self):
        """
        Pide al GestorRutas el fondo de combate (incluye Boss Final)
        """
        jugador = self.obtener_jugador_actual()
        nodo = getattr(jugador, "nodo_actual", "Comedor")
        
        # Llamamos al gestor indicando que SI es combate
        return self.rutas.obtener_ruta_fondo(nodo, es_combate=True)
    
    # --- EN Modelos.py ---

    # --- EN Modelos.py ---

    def procesar_movimiento(self, nombre_nodo):
        """
        Valida si el movimiento es posible antes de ejecutarlo.
        """
        jugador = self.obtener_jugador_actual()
        if not jugador: return {"Tipo": "Nada"}

        # --- VALIDACIÓN DE CONEXIÓN ---
        # Obtenemos las rutas que están unidas al nodo donde está el jugador ahora
        caminos_validos = self.encuentros.rutas_posibles(jugador.nodo_actual)
        
        # Si el usuario hace clic en un nodo lejano o no conectado, no hacemos nada
        if nombre_nodo not in caminos_validos:
            print(f"Movimiento inválido: {jugador.nodo_actual} no está unido a {nombre_nodo}")
            return {"Tipo": "Nada"} 

        # --- EJECUCIÓN DEL MOVIMIENTO ---
        jugador.nodo_actual = nombre_nodo
        print(f"Moviendo a: {nombre_nodo}")
        
        # Generamos el evento del nuevo nodo
        resultado = self.encuentros.generar_decision(nombre_nodo)
        
        if resultado["Tipo"] == "Muerte":
            jugador.vidas -= 1
            if jugador.vidas <= 0:
                jugador.vivo = False
                
        elif resultado["Tipo"] == "Premio":
            resultado["SubioNivel"] = jugador.ganar_xp(resultado["Cantidad"])
        
        # Solo cambiamos de turno si el movimiento fue exitoso
        self.cambiar_turno()
        return resultado

    def guardar_todo(self):
        return self.datos.guardar_partida(self.jugadores)