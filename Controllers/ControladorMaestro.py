import pygame
import sys

# Importación de Modelos, Vistas y Controladores
from Models.Modelos import GameModel
from Views.Interfaz_conf import Interfaz_conf
from Views.Menu_Vista import Menu_Vista
from Views.Juego_Vista import GameView
from Views.Estructura_Vista import Estructura_Vista
from Views.Combate_Vista import Combate_Vista

from Controllers.MenuControlador import MenuControlador
from Controllers.MapControlador import Mapcontrolador
from Controllers.EvolucionControlador import EvolucionControlador
from Controllers.CombateControlador import CombateControlador

class ControladorMaestro:
    def __init__(self):
        pygame.init()
        self.config = Interfaz_conf()
        
        # Parche de seguridad para fuentes
        if not hasattr(self.config, 'f_media'):
            self.config.f_media = self.config.f_chica

        self.ventana = pygame.display.set_mode((930, 600))
        pygame.display.set_caption("ECOS DE LA CARTA")
        self.reloj = pygame.time.Clock()

        # Inicialización del Modelo
        self.model = GameModel()
        
        # Vistas
        self.v_menu = Menu_Vista(self.config)
        self.v_juego = GameView(self.config)
        self.v_estructuras = Estructura_Vista(self.config)
        self.v_combate = Combate_Vista(self.config)

        # Controladores
        self.c_menu = MenuControlador(self.model)
        self.c_mapa = Mapcontrolador(self.model, self.v_estructuras)
        self.c_evolucion = EvolucionControlador(self.model)
        self.c_combate = None 
        
        self.estado = "MENU"
        self.msg_muerte = ""

    def ejecutar(self):
        """Bucle principal."""
        while True:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self._guardar_progreso()
                    pygame.quit()
                    sys.exit()

            self._gestionar_estados(eventos)
            self._dibujar()
            
            pygame.display.flip()
            self.reloj.tick(60)

    def _gestionar_estados(self, eventos):
        """Maneja las transiciones de pantalla."""
        if self.estado == "MENU":
            res = self.c_menu.inicio(eventos)
            if res == "SELECCION": self.estado = "SELECCION"

        elif self.estado == "SELECCION":
            res = self.c_menu.seleccion(eventos)
            if res == "JUEGO": 
                self._guardar_progreso()
                self.estado = "JUEGO"

        elif self.estado == "JUEGO":
            res = self.c_mapa.gestionar_movimiento(eventos)
            if res:
                if res["Tipo"] == "Combate":
                    self.c_combate = CombateControlador(self.model, self.v_combate)
                    self.estado = "COMBATE"
                elif res["Tipo"] == "Muerte":
                    # Aquí se captura el mensaje "¡TE JALASTE EDO!" del modelo
                    self.msg_muerte = res.get("Mensaje", "Has caído")
                    self.estado = "PANTALLA_MUERTE"
                    self._guardar_progreso()
                elif res["Tipo"] == "Premio":
                    if res.get("SubioNivel"): 
                        self.estado = "EVOLUCION"
                    else: 
                        self.model.cambiar_turno()
                    self._guardar_progreso()

        elif self.estado == "COMBATE":
            if self.c_combate:
                res = self.c_combate.ejecutar(eventos)
                if res != "COMBATE":
                    self.estado = res
                    self.c_combate = None
                    self._guardar_progreso()

        elif self.estado == "EVOLUCION":
            res = self.c_evolucion.ejecutar(eventos, self.v_estructuras)
            if res == "JUEGO":
                self.model.cambiar_turno()
                self.estado = "JUEGO"
                self._guardar_progreso()
        
        elif self.estado == "PANTALLA_MUERTE":
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    # Si el botón de la vista muerte fue presionado
                    if self.v_estructuras.rect_boton_muerte.collidepoint(evento.pos):
                        p = self.model.obtener_jugador_actual()
                        if p and p.vidas > 0:
                            self.model.cambiar_turno()
                            self.estado = "JUEGO"
                        else:
                            self.__init__() # Reset total
                            self.estado = "MENU"

    def _guardar_progreso(self):
        """Persistencia en JSON."""
        if self.model.jugadores:
            self.model.datos.guardar_sesion(
                self.model.jugadores, 
                self.model.modo_juego, 
                self.model.turno_actual
            )

    def _dibujar(self):
        """Renderizado según estado."""
        self.ventana.fill(self.config.NEGRO)

        if self.estado == "MENU":
            self.v_menu.dibujar_menu(self.ventana, self.model)
        
        elif self.estado == "SELECCION":
            self.v_menu.dibujar_seleccion_clase(self.ventana, self.model)
        
        elif self.estado in ["JUEGO", "EVOLUCION"]:
            self.v_juego.dibujar_interfaz(self.ventana, self.model)
            if self.estado == "JUEGO":
                self.v_estructuras.dibujar_mapa_grafo(self.ventana, self.model)
            else:
                self.v_estructuras.dibujar_arbol_habilidades(self.ventana, self.model)
        
        elif self.estado == "COMBATE":
            if self.c_combate:
                self.v_combate.dibujar_combate(self.ventana, self.model, self.c_combate.log_daño)
        
        elif self.estado == "PANTALLA_MUERTE":
            self.v_estructuras.dibujar_pantalla_muerte(self.ventana, self.model, self.msg_muerte)