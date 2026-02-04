import pygame
import sys

# Importacion de Modelos, Vistas y Controladores
from Models.Modelos import GameModel
from Views.Interfaz_conf import Interfaz_conf
from Views.Menu_Vista import Menu_Vista
from Views.Juego_Vista import GameView
from Views.Estructura_Vista import Estructura_Vista
from Views.Combate_Vista import Combate_Vista
from Views.Vista_Final import Vista_Final 

from Controllers.MenuControlador import MenuControlador
from Controllers.MapControlador import Mapcontrolador
from Controllers.EvolucionControlador import EvolucionControlador
from Controllers.CombateControlador import CombateControlador

class ControladorMaestro:
    def __init__(self):
        # 1. INICIALIZACION DEL MOTOR Y CONFIGURACION
        pygame.init()
        self.config = Interfaz_conf()
        
        # Parche para asegurar que las fuentes existan antes de renderizar
        if not hasattr(self.config, 'f_media'):
            self.config.f_media = self.config.f_chica

        # Creacion de la superficie principal y reloj de control de tiempo
        self.ventana = pygame.display.set_mode((930, 600))
        pygame.display.set_caption("ECOS DE LA CARTA")
        self.reloj = pygame.time.Clock()

        # 2. INICIALIZACION DE LA ARQUITECTURA (MVC)
        # El Modelo centraliza los datos del juego
        self.model = GameModel()
        
        # Inicializacion de todas las capas visuales
        self.v_menu = Menu_Vista(self.config)
        self.v_juego = GameView(self.config)
        self.v_estructuras = Estructura_Vista(self.config)
        self.v_combate = Combate_Vista(self.config)
        self.v_final = Vista_Final(self.config) 

        # Registro de controladores especificos para cada modulo
        self.c_menu = MenuControlador(self.model)
        self.c_mapa = Mapcontrolador(self.model, self.v_estructuras)
        self.c_evolucion = EvolucionControlador(self.model)
        self.c_combate = None # Se instancia dinamicamente al iniciar pelea
        
        # 3. CONTROL DE ESTADOS Y TEXTOS DINAMICOS
        # Estos textos se llenan con la info que viene del SistemaEncuentros
        self.estado = "MENU"
        self.msg_muerte = ""
        self.titulo_muerte = "" 

    def ejecutar(self):
        """Bucle infinito que mantiene el proceso vivo"""
        while True:
            # Captura de eventos de entrada (Teclado, Mouse, Ventana)
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self._guardar_progreso()
                    pygame.quit()
                    sys.exit()

            # Procesamiento de logica y renderizado
            self._gestionar_estados(eventos)
            self._dibujar()
            
            # Actualizacion de pantalla a 60 cuadros por segundo
            pygame.display.flip()
            self.reloj.tick(60)

    def _gestionar_estados(self, eventos):
        """Maquina de estados que decide que controlador tiene el mando"""
        
        if self.estado == "MENU":
            res = self.c_menu.inicio(eventos)
            if res == "SELECCION": self.estado = "SELECCION"

        elif self.estado == "SELECCION":
            res = self.c_menu.seleccion(eventos)
            if res == "JUEGO": 
                self._guardar_progreso()
                self.estado = "JUEGO"

        elif self.estado == "JUEGO":
            # El controlador de mapa nos dice que evento encontro el jugador
            res = self.c_mapa.gestionar_movimiento(eventos)
            if res:
                # Sincronizamos los mensajes de derrota definidos en el Modelo
                self.msg_muerte = res.get("Mensaje", "HAS CAIDO")
                
                if res["Tipo"] == "Combate":
                    # Cambia a combate y guarda el titulo (ej: PROYECTO RECHAZADO)
                    self.titulo_muerte = res.get("TituloMuerte", "FALLO ACADEMICO")
                    self.c_combate = CombateControlador(self.model, self.v_combate)
                    self.estado = "COMBATE"
                elif res["Tipo"] == "Muerte":
                    # Muerte por trampa: directo a pantalla de derrota
                    self.titulo_muerte = res.get("Titulo", "FALLO ACADEMICO")
                    self.estado = "PANTALLA_MUERTE"
                    self._guardar_progreso()
                elif res["Tipo"] == "Premio":
                    # Si el premio da suficiente XP para nivel, vamos a EVOLUCION
                    if res.get("SubioNivel"): 
                        self.estado = "EVOLUCION"
                    self._guardar_progreso()

        elif self.estado == "COMBATE":
            if self.c_combate:
                res = self.c_combate.ejecutar(eventos)
                if res != "COMBATE":
                    if self.c_combate.victoria:
                        jugador = self.model.obtener_jugador_actual()
                        # Si vence a Boris en el Piso 5, termina el juego
                        if getattr(jugador, "nodo_actual", "") == "Piso 5":
                            self.estado = "VICTORIA_FINAL"
                        else:
                            self.estado = res 
                    elif self.c_combate.derrota:
                        # Los textos de muerte ya se guardaron al entrar al nodo
                        self.estado = "PANTALLA_MUERTE"
                    
                    self.c_combate = None
                    self._guardar_progreso()

        elif self.estado == "EVOLUCION":
            res = self.c_evolucion.ejecutar(eventos, self.v_estructuras)
            if res == "JUEGO":
                self.estado = "JUEGO"
                self._guardar_progreso()
        
        elif self.estado == "PANTALLA_MUERTE":
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    # Detectamos clic en el boton de reintento/salida
                    if self.v_estructuras.rect_boton_muerte.collidepoint(evento.pos):
                        jugador_actual = self.model.obtener_jugador_actual()
                        hay_vivos = self.model.verificar_sobrevivientes()

                        if jugador_actual.vidas <= 0:
                            # Si no hay vidas, revisamos si el compañero sigue vivo (Modo 2P)
                            if self.model.modo_juego == 2 and hay_vivos:
                                self.model.cambiar_turno()
                                self.estado = "JUEGO"
                            else:
                                # Game Over total: reiniciamos el objeto Controlador
                                self.__init__() 
                                self.estado = "MENU"
                        else:
                            # Aun tiene corazones: vuelve al mapa
                            self.estado = "JUEGO"
                        self._guardar_progreso()

        elif self.estado == "VICTORIA_FINAL":
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.v_final.rect_boton_fin.collidepoint(evento.pos):
                        self.__init__()
                        self.estado = "MENU"

    def _guardar_progreso(self):
        """Llama al sistema de archivos para salvar la partida en JSON"""
        if self.model.jugadores:
            self.model.datos.guardar_sesion(
                self.model.jugadores, 
                self.model.modo_juego, 
                self.model.turno_actual
            )

    def _dibujar(self):
        """Selecciona que vista dibujar en la ventana segun el estado"""
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
            # Pasamos los textos capturados del modelo a la vista de muerte
            self.v_estructuras.dibujar_pantalla_muerte(
                self.ventana, 
                self.model, 
                self.msg_muerte, 
                self.titulo_muerte
            )
        elif self.estado == "VICTORIA_FINAL":
            self.v_final.dibujar_victoria(self.ventana, self.model)