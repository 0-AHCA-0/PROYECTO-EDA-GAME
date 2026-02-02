import pygame
import sys
# Importamos el Modelo Central
from Models.Modelos import GameModel
from Views.Interfaz_conf import Interfaz_conf

# Importamos Vistas
from Views.Menu_Vista import Menu_Vista
from Views.Juego_Vista import GameView
from Views.Estructura_Vista import Estructura_Vista
from Views.Combate_Vista import Combate_Vista

# Importamos Controladores
from Controllers.MenuControlador import MenuControlador
from Controllers.MapControlador import Mapcontrolador
from Controllers.EvolucionControlador import EvolucionControlador
from Controllers.CombateControlador import CombateControlador

class JuegoEcos:
    def __init__(self):
        pygame.init()
        self.ventana = pygame.display.set_mode((930, 600))
        pygame.display.set_caption("ECOS DE LA CARTA")
        self.reloj = pygame.time.Clock()

        # 1. Componentes de Datos y Configuración
        self.config = Interfaz_conf()
        self.model = GameModel()
        
        # 2. Instanciar Vistas
        self.v_menu = Menu_Vista(self.config)
        self.v_juego = GameView(self.config)
        self.v_estructuras = Estructura_Vista(self.config)
        self.v_combate = Combate_Vista(self.config)

        # 3. Instanciar Controladores
        self.c_menu = MenuControlador(self.model)
        self.c_mapa = Mapcontrolador(self.model, self.v_estructuras)
        self.c_evolucion = EvolucionControlador(self.model)
        self.c_combate = None # Se crea solo cuando entramos en combate

        self.estado = "MENU"

    def ejecutar(self):
        ejecutando = True
        while ejecutando:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    ejecutando = False
                
                # --- LÓGICA DE CLIC PARA PANTALLA DE MUERTE ---
                if self.estado == "PANTALLA_MUERTE":
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if hasattr(self.v_estructuras, 'rect_boton_muerte'):
                            if self.v_estructuras.rect_boton_muerte.collidepoint(evento.pos):
                                if self.model.verificar_sobrevivientes():
                                    self.model.cambiar_turno() # Ahora el turno cambia SOLO aquí
                                    self.estado = "JUEGO"
                                else:
                                    self.estado = "MENU"

            # --- MÁQUINA DE ESTADOS (CONTROLADORES) ---
            if self.estado == "MENU":
                self.estado = self.c_menu.inicio(eventos)
            
            elif self.estado == "SELECCION":
                self.estado = self.c_menu.seleccion(eventos)
            
            elif self.estado == "JUEGO":
                resultado = self.c_mapa.gestionar_movimiento(eventos)
                if resultado:
                    if resultado.get("Tipo") == "Combate":
                        self.c_combate = CombateControlador(self.model, self.v_combate)
                        self.estado = "COMBATE"
                    elif resultado.get("Tipo") == "Muerte" and not self.model.obtener_jugador_actual().vivo:
                        self.estado = "PANTALLA_MUERTE"
                    elif resultado.get("SubioNivel"):
                        self.estado = "EVOLUCION"

            elif self.estado == "EVOLUCION":
                self.estado = self.c_evolucion.ejecutar(eventos, self.v_estructuras)


            elif self.estado == "COMBATE":
                if self.c_combate:
                    # Ejecutamos la lógica y recibimos el siguiente estado
                    nuevo_estado = self.c_combate.ejecutar(eventos)
                    
                    if nuevo_estado == "PANTALLA_MUERTE":
                        self.estado = "PANTALLA_MUERTE"
                        self.c_combate = None # Limpiamos el controlador de combate
                    elif nuevo_estado == "JUEGO":
                        self.estado = "JUEGO"
                        self.c_combate = None

            # --- RENDERIZADO (VISTAS) ---
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
                # Dibujamos el fondo del juego estático y encima el cartel de muerte
                self.v_juego.dibujar_interfaz(self.ventana, self.model)
                self.v_estructuras.dibujar_pantalla_muerte(self.ventana, self.model)

            pygame.display.flip()
            self.reloj.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    juego = JuegoEcos()
    juego.ejecutar()