import pygame
import math
import os

class GameView:
    def __init__(self, config):
        self.c = config
        self.ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def dibujar_interfaz(self, ventana, jugador, nombre_carta_actual):
        # 1. DIBUJAR EL FONDO DE JUEGO
        try:
            ruta_fondo = os.path.join(self.ruta_proyecto, "Imagenes", "Fondo_Inicial.png")
            fondo = pygame.image.load(ruta_fondo)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
        except Exception as e:
            print(f"Error al cargar fondo_juego.png: {e}")
            ventana.fill((160, 140, 90)) # Color tablero por defecto

        # 2. LÓGICA DE LA CARTA FLOTANTE (Efecto Seno)
        # Usamos el tiempo de Pygame para crear un movimiento suave en el eje Y
        tiempo = pygame.time.get_ticks() / 1000  
        flotacion = math.sin(tiempo) * 8  # Intensidad del movimiento
        
        x_carta = 100
        y_carta = int(150 + flotacion)
        rect_carta = pygame.Rect(x_carta, y_carta, 230, 320)
        
        # Dibujo del marco de la carta
        pygame.draw.rect(ventana, (20, 20, 20), rect_carta) 
        COLOR_DORADO = (218, 165, 32)
        pygame.draw.rect(ventana, COLOR_DORADO, rect_carta, 8) 

        # 3. CARGA DINÁMICA DE LA IMAGEN DE LA CARTA
        try:
            # Mapeo de clases a archivos de imagen
            mapeo_clases = {
                "Fuego": "P_Fuego.png",
                "Agua": "P_Agua.png",
                "Tierra": "P_Tierra.png",
                "Aire": "P_Aire.png"
            }
            # Obtener el archivo de imagen basado en la clase del jugador
            nombre_archivo = mapeo_clases.get(jugador.clase, "P_Fuego.png")
            ruta_img = os.path.join(self.ruta_proyecto, "Imagenes", nombre_archivo)
            imagen_carta = pygame.image.load(ruta_img)
            imagen_carta = pygame.transform.scale(imagen_carta, (200, 220))
            ventana.blit(imagen_carta, (x_carta + 15, y_carta + 20))
        except Exception as e:
            # Placeholder si no hay imagen todavía
            print(f"Error cargando imagen: {e}")
            pygame.draw.rect(ventana, (100, 100, 100), (x_carta + 15, y_carta + 20, 200, 220))

        # Nombre de la carta sobre el marco
        txt_nombre = self.c.f_chica.render(nombre_carta_actual, True, self.c.NEGRO)
        ventana.blit(txt_nombre, (x_carta, y_carta - 30))

        # 4. ESTADÍSTICAS (LP y EXP)
        # Estilo Impact para los Life Points (LP)
        fuente_lp = pygame.font.SysFont("Impact", 60)
        lp_texto = f"LP: {jugador.vidas}000"
        
        # Sombra y Texto Neón
        render_sombra = fuente_lp.render(lp_texto, True, self.c.NEGRO)
        render_lp = fuente_lp.render(lp_texto, True, self.c.NEON)
        ventana.blit(render_sombra, (455, 205)) 
        ventana.blit(render_lp, (450, 200))

        # Barra de Experiencia (EXP)
        xp_actual = getattr(jugador, 'xp', 0)
        txt_xp = self.c.f_chica.render(f"EXP: {xp_actual}/100", True, self.c.BLANCO)
        pygame.draw.rect(ventana, self.c.NEGRO, (440, 270, 200, 40))
        ventana.blit(txt_xp, (450, 280))

        # 5. CAJA DE STATS INFERIOR (ATK/DEF)
        rect_stats = pygame.Rect(x_carta + 20, y_carta + 250, 190, 50)
        pygame.draw.rect(ventana, (240, 230, 140), rect_stats)
        txt_atk_def = self.c.f_chica.render("ATK/900  DEF/400", True, self.c.NEGRO)
        ventana.blit(txt_atk_def, (x_carta + 30, y_carta + 260))