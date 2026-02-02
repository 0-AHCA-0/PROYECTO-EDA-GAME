import pygame
import sys

# Traemos todo lo necesario
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
        self.ventana = pygame.display.set_mode((930, 600))
        pygame.display.set_caption("ECOS DE LA CARTA")
        self.reloj = pygame.time.Clock()

        # El cerebro de los datos
        self.model = GameModel()
        
        # Seteamos las vistas
        self.v_menu = Menu_Vista(self.config)
        self.v_juego = GameView(self.config)
        self.v_estructuras = Estructura_Vista(self.config)
        self.v_combate = Combate_Vista(self.config)

        # Controladores iniciales
        self.c_menu = MenuControlador(self.model)
        self.c_mapa = Mapcontrolador(self.model, self.v_estructuras)
        self.c_evolucion = EvolucionControlador(self.model)
        
        # El estado inicial siempre es el MENU
        self.estado = "MENU"
        self.c_combate = None
        self.mensaje_muerte = ""

    def ejecutar(self):
        # El bucle principal del juego
        while True:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self._actualizar(eventos)
            self._renderizar()
            
            pygame.display.flip()
            self.reloj.tick(60)

    def _actualizar(self, eventos):
        # Aca manejamos a donde va el jugador
        if self.estado == "MENU":
            self.estado = self.c_menu.inicio(eventos)
        
        elif self.estado == "SELECCION":
            self.estado = self.c_menu.seleccion(eventos)

        elif self.estado == "JUEGO":
            res = self.c_mapa.gestionar_movimiento(eventos)
            if res:
                if res["Tipo"] == "Combate":
                    self.c_combate = CombateControlador(self.model, self.v_combate)
                    self.estado = "COMBATE"
                elif res["Tipo"] == "Muerte":
                    self.mensaje_muerte = res["Mensaje"]
                    self.estado = "PANTALLA_MUERTE"
                elif res.get("SubioNivel"):
                    self.estado = "EVOLUCION"

        elif self.estado == "EVOLUCION":
            self.estado = self.c_evolucion.ejecutar(eventos, self.v_estructuras)

        elif self.estado == "COMBATE":
            if self.c_combate:
                nuevo = self.c_combate.ejecutar(eventos)
                if nuevo != "COMBATE":
                    # Si perdio en combate, guardamos el log para mostrarlo
                    if nuevo == "PANTALLA_MUERTE":
                        self.mensaje_muerte = self.c_combate.log_daño
                    self.estado = nuevo
                    self.c_combate = None

        elif self.estado == "PANTALLA_MUERTE":
            for ev in eventos:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    # Si toca el boton de la pantalla de muerte
                    if self.v_estructuras.rect_boton_muerte.collidepoint(ev.pos):
                        jugador = self.model.obtener_jugador_actual()
                        
                        # Si todavia tiene corazones, vuelve al mapa
                        if jugador.vidas > 0:
                            self.estado = "JUEGO"
                        # Si es 2P y el otro sigue vivo, cambia el turno
                        elif self.model.modo_juego == 2 and self.model.verificar_sobrevivientes():
                            self.model.cambiar_turno()
                            self.estado = "JUEGO"
                        else:
                            # Game Over total, reseteamos todo el objeto
                            self.__init__() 
                            self.estado = "MENU"

    def _renderizar(self):
        # Dibujamos todo segun el estado
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
                self.v_combate.dibujar_enemigo_vida(self.ventana, self.c_combate.enemigo)

        elif self.estado == "PANTALLA_MUERTE":
            self.v_juego.dibujar_interfaz(self.ventana, self.model)
            self.v_estructuras.dibujar_pantalla_muerte(self.ventana, self.model, self.mensaje_muerte)