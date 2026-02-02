import pygame
import math

class GameView:
    def __init__(self, config):
        self.c = config

    def dibujar_interfaz(self, ventana, modelo):
        """
        Renderizado sincronizado: LPs numéricos y Corazones para vidas globales.
        """
        jugador = modelo.obtener_jugador_actual()
        if not jugador: return

        # 1. FONDO (Dinámico según el nodo)
        try:
            ruta_fondo = modelo.obtener_ruta_fondo_nodo()
            fondo = pygame.image.load(ruta_fondo)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
        except Exception:
            ventana.fill((40, 40, 40)) # Fondo oscuro si falla

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
        ventana.blit(txt_nombre, (x_carta + (230 - txt_nombre.get_width())//2, y_carta - 30))

        # ---------------------------------------------------------
        # 4. UI SINCRONIZADA (Vidas Globales y LPs)
        # ---------------------------------------------------------
        x_info_base = 360 
        
        # --- A. VIDAS GLOBALES (Corazones) ---
        # Dibujamos corazones pequeños para representar las "vidas" (3 intentos)
        txt_vidas_glob = self.c.f_chica.render("VIDAS:", True, self.c.BLANCO)
        ventana.blit(txt_vidas_glob, (x_info_base, 150))
        
        for i in range(jugador.vidas):
            # Si tienes una imagen de corazón: ventana.blit(img, (x, y))
            # Por ahora usamos círculos rojos como placeholders de corazones
            pygame.draw.circle(ventana, (255, 50, 50), (x_info_base + 80 + (i * 25), 160), 8)

        # --- B. PUNTOS DE VIDA (LPs Reales) ---
        # Mostramos los LPs que se usarán en el combate
        fuente_lp = pygame.font.SysFont("Impact", 50)
        # Color Neón si tiene mucha vida, rojo si tiene poca
        color_vida = self.c.NEON if jugador.vida > 30 else (255, 0, 0)
        
        texto_lp = fuente_lp.render(f"{int(jugador.vida)} LP", True, color_vida)
        ventana.blit(texto_lp, (x_info_base, 180))
        
        # --- C. UBICACIÓN Y XP ---
        nodo_actual = getattr(jugador, "nodo_actual", "Inicio")
        txt_ubi = self.c.f_chica.render(f"UBICACIÓN: {nodo_actual}", True, self.c.BLANCO)
        ventana.blit(txt_ubi, (x_info_base, 245))
        
        # Barra XP
        xp_actual = jugador.xp
        xp_maxima = 100
        ancho_barra_max = 200
        progreso = (xp_actual / xp_maxima) * ancho_barra_max
        
        txt_xp = self.c.f_chica.render(f"EXP: {xp_actual} / {xp_maxima}", True, self.c.BLANCO)
        ventana.blit(txt_xp, (x_info_base, 280))
        
        pygame.draw.rect(ventana, self.c.NEGRO, (x_info_base, 310, ancho_barra_max, 12)) 
        pygame.draw.rect(ventana, self.c.BLANCO, (x_info_base, 310, progreso, 12))