import pygame
import os
import math

class Combate_Vista:
    def __init__(self, config):
        self.c = config
        self.ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Rectángulo para el botón de ataque
        self.rect_boton_hab = pygame.Rect(350, 480, 230, 60)

    def dibujar_combate(self, ventana, jugador, enemigo, log_daño):
        # 1. FONDO
        try:
            ruta_fondo = os.path.join(self.ruta_proyecto, "Imagenes", "Fondo_Universidad.png")
            fondo = pygame.image.load(ruta_fondo)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
        except:
            ventana.fill((30, 10, 10))

        # 2. DIBUJAR PERSONAJES (Efecto flotante)
        tiempo = pygame.time.get_ticks() / 1000
        flotacion = math.sin(tiempo) * 10
        
        # Jugador
        try:
            ruta_p = os.path.join(self.ruta_proyecto, "Imagenes", f"P_{jugador.clase}.png")
            img_p = pygame.image.load(ruta_p)
            img_p = pygame.transform.scale(img_p, (200, 260))
            ventana.blit(img_p, (100, 150 + flotacion))
        except:
            pygame.draw.rect(ventana, (0, 255, 0), (100, 150 + flotacion, 200, 260))

        # Enemigo
        try:
            ruta_e = os.path.join(self.ruta_proyecto, "Imagenes", "Enemigo.png")
            img_e = pygame.image.load(ruta_e)
            img_e = pygame.transform.scale(img_e, (200, 260))
            ventana.blit(img_e, (630, 150 - flotacion))
        except:
            pygame.draw.rect(ventana, (255, 0, 0), (630, 150 - flotacion, 200, 260))

        # 3. BARRAS DE VIDA (Aquí es donde fallaba)
        # TÚ: usa .vidas (cantidad de corazones)
        self._barra_vida(ventana, 100, 450, jugador.vidas, jugador.vidas_max, (0, 255, 0), "TU VIDA")
        
        # ENEMIGO: usa .vida (puntos numéricos)
        self._barra_vida(ventana, 630, 450, enemigo.vida, enemigo.vidas_max, (255, 0, 0), enemigo.nombre)

        # 4. BOTÓN DE ATAQUE
        pygame.draw.rect(ventana, self.c.NEON, self.rect_boton_hab, border_radius=10)
        txt_boton = self.c.f_chica.render(f"ATACAR CON {jugador.habilidad_actual}", True, self.c.NEGRO)

        # centrado del boton
        txt_rect = txt_boton.get_rect(center=self.rect_boton_hab.center)
        ventana.blit(txt_boton, txt_rect)

        # 5. LOG DE COMBATE
        txt_log = self.c.f_chica.render(log_daño, True, self.c.BLANCO)
        ventana.blit(txt_log, (465 - txt_log.get_width()//2, 50))

    # --- MÉTODO QUE FALTABA ---
    def _barra_vida(self, ventana, x, y, actual, maximo, color, nombre):
        """Dibuja la barra de salud proporcional"""
        ancho_total = 200
        # Evitar división por cero
        ratio = max(0, min(actual / maximo if maximo > 0 else 0, 1))
        
        # Fondo gris
        pygame.draw.rect(ventana, (50, 50, 50), (x, y, ancho_total, 20), border_radius=5)
        # Barra de color
        if ratio > 0:
            pygame.draw.rect(ventana, color, (x, y, int(ancho_total * ratio), 20), border_radius=5)
        
        # Texto del nombre
        txt = self.c.f_chica.render(f"{nombre}: {actual}", True, self.c.BLANCO)
        ventana.blit(txt, (x, y - 25))

    def dibujar_derrota(self, ventana, msj):
        ventana.fill((50, 0, 0))
        txt = self.c.f_grande.render("GAME OVER", True, (255, 255, 255))
        ventana.blit(txt, (300, 250))