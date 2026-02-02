import pygame
import math

class GameView:
    def __init__(self, config):
        self.c = config
        # ¡ADIÓS a os.path, self.ruta_proyecto y ArbolEvolucion local!

    def dibujar_interfaz(self, ventana, modelo):
        """
        Versión Senior: Renderizado limpio sin solapamientos entre UI y Grafo.
        """
        jugador = modelo.obtener_jugador_actual()
        if not jugador: return

        # 1. FONDO (Dinámico según el nodo del grafo)
        try:
            ruta_fondo = modelo.obtener_ruta_fondo_nodo()
            fondo = pygame.image.load(ruta_fondo)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
        except Exception as e:
            ventana.fill((160, 140, 90))

        # 2. CARTA PERSONAJE (Efecto de flotación)
        tiempo = pygame.time.get_ticks() / 1000  
        flotacion = math.sin(tiempo) * 8  
        x_carta, y_carta = 100, int(150 + flotacion)
        
        try:
            ruta_personaje = modelo.obtener_ruta_imagen_personaje()
            personaje = pygame.image.load(ruta_personaje)
            personaje = pygame.transform.scale(personaje, (230, 320))
            ventana.blit(personaje, (x_carta, y_carta))
        except:
            pygame.draw.rect(ventana, (100, 100, 100), (x_carta, y_carta, 230, 320))

        # 3. NOMBRE DE EVOLUCIÓN (Encima de la carta)
        nombre_evolucion = modelo.info_visual()
        txt_nombre = self.c.f_chica.render(nombre_evolucion, True, self.c.BLANCO)
        ancho_txt = txt_nombre.get_width()
        ventana.blit(txt_nombre, (x_carta + (230 - ancho_txt)//2, y_carta - 30))

        # ---------------------------------------------------------
        # 4. UI AJUSTADA (Vida, XP, Ubicación) - MOVIDA A LA IZQUIERDA
        # ---------------------------------------------------------
        nodo_actual = getattr(jugador, "nodo_actual", "Inicio")
        xp_actual = getattr(jugador, "xp", 0)
        x_info_base = 360 # Movido de 450 a 360 para evitar al Grafo
        
        # Vida (LP) - Ajustado tamaño para que sea más elegante
        fuente_lp = pygame.font.SysFont("Impact", 50)
        ventana.blit(fuente_lp.render(f"LP: {jugador.vidas}000", True, self.c.NEON), (x_info_base, 180))
        
        # Ubicación
        txt_ubi = self.c.f_chica.render(f"UBICACIÓN: {nodo_actual}", True, self.c.BLANCO)
        ventana.blit(txt_ubi, (x_info_base, 245))
        
        # Barra XP (Compacta)
        xp_maxima = 100
        ancho_barra_max = 200 # Reducida de 270 a 200
        progreso = (xp_actual / xp_maxima) * ancho_barra_max
        
        txt_xp = self.c.f_chica.render(f"EXP: {xp_actual} / {xp_maxima}", True, self.c.BLANCO)
        ventana.blit(txt_xp, (x_info_base, 280))
        
        # Dibujar rectángulos de la barra
        pygame.draw.rect(ventana, self.c.NEGRO, (x_info_base, 310, ancho_barra_max, 12)) 
        pygame.draw.rect(ventana, self.c.BLANCO, (x_info_base, 310, progreso, 12))