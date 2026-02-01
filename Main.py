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
        self.c_evo = EvolucionControlador(self.model)
        self.c_combate = None 

        # Estado inicial
        self.estado = "MENU"
        self.ejecutando = True

    def ejecutar(self):
        while self.ejecutando:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.ejecutando = False

            # ==========================================
            # 1. LÓGICA DE CONTROLADORES (Inputs)
            # ==========================================
            if self.estado == "MENU":
                # Retorna "SELECCION" si se elige 1P o 2P
                self.estado = self.c_menu.inicio(eventos)
            
            elif self.estado == "SELECCION":
                # Retorna "JUEGO" cuando se eligen las clases
                self.estado = self.c_menu.seleccion(eventos)
            
            elif self.estado == "JUEGO":
                # Retorna dict con evento {Tipo: "Combate"|"Premio"|"Muerte"}
                resultado = self.c_mapa.gestionar_movimiento(eventos)
                if resultado:
                    if resultado["Tipo"] == "Combate":
                        # Iniciamos el controlador de combate
                        self.c_combate = CombateControlador(self.model, self.v_combate)
                        self.estado = "COMBATE"
                    elif resultado["Tipo"] == "Muerte":
                        self.estado = "DERROTA"
                    elif resultado.get("SubioNivel"):
                        self.estado = "EVOLUCION"

            elif self.estado == "COMBATE":
                if self.c_combate:
                    # Ejecuta lógica de turnos y retorna "JUEGO" si gana o "DERROTA" si pierde
                    self.estado = self.c_combate.ejecutar(eventos)
                else:
                    self.estado = "JUEGO"

            elif self.estado == "EVOLUCION":
                # Retorna "JUEGO" una vez elegida la habilidad
                self.estado = self.c_evo.ejecutar(eventos, self.v_estructuras)


            # ==========================================
            # 2. RENDERIZADO (Dibujo en Pantalla)
            # ==========================================
            self.ventana.fill(self.config.NEGRO)

            if self.estado == "MENU":
                # CAMBIO: Pasamos self.model para que busque el fondo
                self.v_menu.dibujar_menu(self.ventana, self.model)
            
            elif self.estado == "SELECCION":
                # CAMBIO: Pasamos self.model para cargar imágenes dinámicas de clases
                self.v_menu.dibujar_seleccion_clase(self.ventana, self.model)
            
            elif self.estado in ["JUEGO", "EVOLUCION"]:
                # CAMBIO: Simplificado. La vista extrae todo del modelo.
                self.v_juego.dibujar_interfaz(self.ventana, self.model)
                
                # Dibujamos Grafos o Árboles encima
                if self.estado == "JUEGO":
                    self.v_estructuras.dibujar_mapa_grafo(self.ventana, self.model)
                else: # EVOLUCION
                    self.v_estructuras.dibujar_arbol_habilidades(self.ventana, self.model)
            
            elif self.estado == "COMBATE":
                if self.c_combate:
                    # 1. Dibujamos Fondo, Jugador y Enemigo (Usando Modelo)
                    self.v_combate.dibujar_combate(
                        self.ventana, 
                        self.model, 
                        self.c_combate.log_daño
                    )
                    # 2. Dibujamos la barra de vida del enemigo (Helper extra)
                    self.v_combate.dibujar_enemigo_vida(self.ventana, self.c_combate.enemigo)

            elif self.estado == "DERROTA":
                self.v_combate.dibujar_derrota(self.ventana, "Has caído en combate...")

            pygame.display.flip()
            self.reloj.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    juego = JuegoEcos()
    juego.ejecutar()