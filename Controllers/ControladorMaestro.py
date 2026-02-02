import pygame
import sys

# Importación de modelos y configuración
from Models.Modelos import GameModel
from Views.Interfaz_conf import Interfaz_conf

# Importación de todas las vistas
from Views.Menu_Vista import Menu_Vista
from Views.Juego_Vista import GameView
from Views.Estructura_Vista import Estructura_Vista
from Views.Combate_Vista import Combate_Vista

# Importación de los controladores
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

        self.model = GameModel()
        
        # Inicialización de las Vistas
        self.v_menu = Menu_Vista(self.config)
        self.v_juego = GameView(self.config)
        self.v_estructuras = Estructura_Vista(self.config)
        self.v_combate = Combate_Vista(self.config)

        # Inicialización de Controladores
        self.c_menu = MenuControlador(self.model)
        # CORRECCIÓN: Asegúrate de que el nombre de la clase en MapControlador.py sea Mapcontrolador
        self.c_mapa = Mapcontrolador(self.model, self.v_estructuras)
        self.c_evolucion = EvolucionControlador(self.model)
        self.c_combate = None 
        
        self.estado = "MENU"
        self.mensaje_muerte = ""

    def ejecutar(self):
        while True:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self._actualizar_logica(eventos)
            self._renderizar()

            pygame.display.flip()
            self.reloj.tick(60)

    def _actualizar_logica(self, eventos):
        if self.estado == "MENU":
            nuevo = self.c_menu.inicio(eventos)
            if nuevo: self.estado = nuevo

        elif self.estado == "SELECCION":
            nuevo = self.c_menu.seleccion(eventos)
            if nuevo: self.estado = nuevo

        elif self.estado == "JUEGO":
            resultado = self.c_mapa.gestionar_movimiento(eventos)
            if resultado:
                # El modelo retorna un dict con el tipo de encuentro
                if resultado.get("Tipo") == "Combate":
                    self.c_combate = CombateControlador(self.model, self.v_combate)
                    self.estado = "COMBATE"
                elif resultado.get("Tipo") == "Muerte":
                    self.mensaje_muerte = resultado.get("Mensaje", "Has caído")
                    self.estado = "PANTALLA_MUERTE"
                
                # Verificar si subió de nivel para ir a evolución
                if resultado.get("SubioNivel"):
                    self.estado = "EVOLUCION"

        elif self.estado == "EVOLUCION":
            # Pasamos la vista porque el controlador necesita los rects de los botones
            nuevo = self.c_evolucion.ejecutar(eventos, self.v_estructuras)
            if nuevo: self.estado = nuevo

        elif self.estado == "COMBATE":
            if self.c_combate:
                nuevo_estado = self.c_combate.ejecutar(eventos)
                if nuevo_estado != "COMBATE":
                    self.estado = nuevo_estado
                    # Limpiamos el controlador de combate al salir
                    self.c_combate = None

        elif self.estado == "PANTALLA_MUERTE":
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    # Usamos el rect que tu Estructura_Vista ya crea en dibujar_pantalla_muerte
                    if self.v_estructuras.rect_boton_muerte.collidepoint(evento.pos):
                        
                        # USAMOS LO QUE YA TIENES: verificar_sobrevivientes del Modelo
                        hay_vivos = self.model.verificar_sobrevivientes()
                        
                        if self.model.modo_juego == 2 and hay_vivos:
                            # Si hay alguien vivo, usamos tu función cambiar_turno()
                            self.model.cambiar_turno()
                            self.estado = "JUEGO"
                        else:
                            # Si es 1P o no queda nadie, reiniciamos todo al menú
                            # Creamos un modelo nuevo para limpiar los datos de la partida
                            self.model = GameModel()
                            # Re-vinculamos los controladores al nuevo modelo
                            self.c_menu = MenuControlador(self.model)
                            self.c_mapa = Mapcontrolador(self.model, self.v_estructuras)
                            self.c_evolucion = EvolucionControlador(self.model)
                            self.estado = "MENU"

    def _renderizar(self):
        self.ventana.fill(self.config.NEGRO)

        if self.estado == "MENU":
            self.v_menu.dibujar_menu(self.ventana, self.model)
        
        elif self.estado == "SELECCION":
            # ¡OJO AQUÍ! Si Menu_Vista no tiene esta función, el juego crashea.
            # Asegúrate de haberla implementado en Menu_Vista.py
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
            self.v_estructuras.dibujar_pantalla_muerte(self.ventana, self.model)