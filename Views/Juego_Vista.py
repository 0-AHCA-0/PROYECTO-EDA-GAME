import pygame
import math

class GameView:
    def __init__(self, config):
        self.c = config
        # ¡ADIÓS a os.path, self.ruta_proyecto y ArbolEvolucion local!

    def dibujar_interfaz(self, ventana, modelo):
        """
        Recibe 'ventana' y el 'modelo' central.
        """
        jugador = modelo.obtener_jugador_actual()
        if not jugador: return

        # 1. FONDO (Pedimos la ruta al modelo)
        try:
            ruta_fondo = modelo.obtener_ruta_fondo_nodo()
            fondo = pygame.image.load(ruta_fondo)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
        except Exception as e:
            print(f"Error fondo: {e}")
            ventana.fill((160, 140, 90))

        # 2. CARTA FLOTANTE
        tiempo = pygame.time.get_ticks() / 1000  
        flotacion = math.sin(tiempo) * 8  
        x_carta, y_carta = 100, int(150 + flotacion)
        
        try:
            # --- MAGIA: Pedimos la imagen exacta al modelo ---
            ruta_personaje = modelo.obtener_ruta_imagen_personaje()
            
            personaje = pygame.image.load(ruta_personaje)
            personaje = pygame.transform.scale(personaje, (230, 320))
            
            # Sombra y Carta
            pygame.draw.rect(ventana, (20, 20, 20), (x_carta + 5, y_carta + 5, 230, 320), border_radius=10)
            ventana.blit(personaje, (x_carta, y_carta))
            
            # Borde según nivel
            colores = {1: self.c.NEON, 2: (255, 215, 0), 3: (255, 50, 50)}
            color_borde = colores.get(int(jugador.nivel_evolucion), self.c.NEON)
            pygame.draw.rect(ventana, color_borde, (x_carta, y_carta, 230, 320), 3, border_radius=10)
        except Exception as e:
            print(f"Error personaje: {e}")
            pygame.draw.rect(ventana, (100, 100, 100), (x_carta, y_carta, 230, 320))

        # 3. TEXTO (Pedimos el nombre "Cool" al modelo)
        nombre_evolucion = modelo.info_visual()
        if nombre_evolucion == "Desconocido": 
            nombre_evolucion = f"{jugador.clase}"

        txt_nombre = self.c.f_chica.render(nombre_evolucion, True, self.c.BLANCO)
        ancho_txt = txt_nombre.get_width()
        ventana.blit(txt_nombre, (x_carta + (230 - ancho_txt)//2, y_carta - 30))

        # 4. UI (Vida, XP, Ubicación)
        nodo_actual = getattr(jugador, "nodo_actual", "Inicio")
        xp_actual = getattr(jugador, "xp", 0)
        
        # Vida
        fuente_lp = pygame.font.SysFont("Impact", 60)
        ventana.blit(fuente_lp.render(f"LP: {jugador.vidas}000", True, self.c.NEON), (450, 180))
        
        # Ubicación
        ventana.blit(self.c.f_chica.render(f"UBICACIÓN: {nodo_actual}", True, self.c.BLANCO), (450, 250))
        
        # Barra XP
        xp_maxima = 100
        ancho_barra = 250
        prop = min(xp_actual / xp_maxima, 1.0)
        
        ventana.blit(self.c.f_chica.render(f"EXP: {xp_actual} / {xp_maxima}", True, self.c.BLANCO), (450, 290))
        pygame.draw.rect(ventana, (50, 50, 50), (450, 320, ancho_barra, 15), border_radius=5)
        if xp_actual > 0:
            pygame.draw.rect(ventana, self.c.NEON, (450, 320, int(ancho_barra * prop), 15), border_radius=5)
        pygame.draw.rect(ventana, self.c.BLANCO, (450, 320, ancho_barra, 15), 1, border_radius=5)