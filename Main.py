import pygame
import sys
from Models.Modelos import GameModel
from Views.Interfaz_conf import Interfaz_conf
from Views.Menu_Vista import Menu_Vista
from Views.Juego_Vista import GameView
from Views.Estructura_Vista import Estructura_Vista
from Views.Combate_Vista import Combate_Vista

# Importamos los controladores
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
        self.c_evo = EvolucionControlador(self.model)
        self.c_combate = None 

        self.estado = "MENU"
        self.ejecutando = True

    def ejecutar(self):
        while self.ejecutando:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.ejecutando = False

            # --- LÓGICA DE ESTADOS ---
            if self.estado == "MENU":
                self.estado = self.c_menu.inicio(eventos)
            
            elif self.estado == "SELECCION":
                self.estado = self.c_menu.seleccion(eventos)
            
            elif self.estado == "JUEGO":
                resultado = self.c_mapa.gestionar_movimiento(eventos)
                if resultado:
                    if resultado["Tipo"] == "Combate":
                        self.c_combate = CombateControlador(self.model, self.v_combate)
                        self.estado = "COMBATE"
                    elif resultado["Tipo"] == "Muerte":
                        self.estado = "DERROTA"
                    elif resultado.get("SubioNivel"):
                        self.estado = "EVOLUCION"

            elif self.estado == "COMBATE":
                if self.c_combate:
                    self.estado = self.c_combate.ejecutar(eventos)
                else:
                    self.estado = "JUEGO"

            elif self.estado == "EVOLUCION":
                self.estado = self.c_evo.ejecutar(eventos, self.v_estructuras)

            # --- RENDERIZADO ---
            self.ventana.fill(self.config.NEGRO)

            if self.estado == "MENU":
                self.v_menu.dibujar_menu(self.ventana)
            
            elif self.estado == "SELECCION":
                self.v_menu.dibujar_seleccion_clase(self.ventana)
            
            # --- CAMBIO AQUÍ: JUEGO Y EVOLUCION COMPARTEN FONDO ---
            elif self.estado in ["JUEGO", "EVOLUCION"]:
                jugador = self.model.obtener_jugador_actual()
                if jugador:
                    nombre_carta = self.model.info_visual()
                    
                    # 1. Dibujamos la interfaz base
                    self.v_juego.dibujar_interfaz(self.ventana, jugador, nombre_carta, jugador.nodo_actual)
                    
                    # 2. Dibujamos el elemento superior según el estado
                    if self.estado == "JUEGO":
                        self.v_estructuras.dibujar_mapa_grafo(self.ventana, self.model)
                    else:
                        # Si es EVOLUCION, el árbol se dibuja encima de la interfaz de Elmo
                        self.v_estructuras.dibujar_arbol_habilidades(self.ventana, self.model)
            
            elif self.estado == "COMBATE":
                jugador = self.model.obtener_jugador_actual()
                if self.c_combate and jugador:
                    self.v_combate.dibujar_combate(
                        self.ventana, 
                        jugador, 
                        self.c_combate.enemigo, 
                        self.c_combate.log_daño
                    )

            elif self.estado == "DERROTA":
                self.v_combate.dibujar_derrota(self.ventana, "Has caído en combate...")

            pygame.display.flip()
            self.reloj.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    juego = JuegoEcos()
    juego.ejecutar()