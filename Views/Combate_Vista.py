import pygame
import os
import math

class Combate_Vista:
    def __init__(self, config):
        self.c = config
        self.ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Rectángulos para detección de clics (Colisiones)
        self.rect_boton_hab = pygame.Rect(350, 480, 230, 60)
        self.rect_boton_reinicio = pygame.Rect(365, 450, 200, 50)

    def dibujar_combate(self, ventana, jugador, enemigo, log_daño):
        """Renderiza la escena de batalla según las instrucciones"""
        # 1. Fondo de batalla personalizado
        try:
            ruta_fondo = os.path.join(self.ruta_proyecto, "Imagenes", "Fondo_Combate.png")
            fondo = pygame.image.load(ruta_fondo)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
        except:
            ventana.fill((40, 20, 20)) # Respaldo visual si no carga la imagen

        # 2. Lógica de la Carta del Jugador (Lado Izquierdo)
        tiempo = pygame.time.get_ticks() / 1000  
        flotacion = math.sin(tiempo) * 10 # Efecto seno para movimiento fluido
        rect_carta = pygame.Rect(100, 150 + flotacion, 220, 310)
        
        # Marco Neón consistente con Interfaz_conf
        pygame.draw.rect(ventana, (10, 10, 10), rect_carta) 
        pygame.draw.rect(ventana, self.c.NEON, rect_carta, 6) 

        # 3. Imagen del Enemigo (Lado Derecho)
        try:
            ruta_ene = os.path.join(self.ruta_proyecto, "Imagenes", "Enemy.png")
            img_ene = pygame.image.load(ruta_ene)
            img_ene = pygame.transform.scale(img_ene, (260, 260))
            ventana.blit(img_ene, (600, 160))
        except:
            # Si no hay imagen, dibuja un círculo representativo
            pygame.draw.circle(ventana, (220, 40, 40), (730, 290), 90)

        # 4. Barras de Salud (LP)
        # Vida Jugador (Basado en Entidades.py)
        self._barra_vida(ventana, 100, 480, jugador.vidas, 10, (50, 255, 50), "Jugador")
        # Vida Enemigo (Basado en el modelo de combate)
        self._barra_vida(ventana, 600, 480, enemigo.vidas, enemigo.vidas_max, (255, 50, 50), "Enemigo")

        # 5. Botón de Habilidad Actual
        pygame.draw.rect(ventana, self.c.NEGRO, self.rect_boton_hab, border_radius=12)
        pygame.draw.rect(ventana, self.c.NEON, self.rect_boton_hab, 3, border_radius=12)
        
        # Muestra dinámicamente la habilidad del grafo
        txt_hab = self.c.f_chica.render(f"HAB: {jugador.habilidad_actual}", True, self.c.BLANCO)
        ventana.blit(txt_hab, (self.rect_boton_hab.x + 15, self.rect_boton_hab.y + 18))

        # 6. Panel de Log de Daño
        txt_log = self.c.f_chica.render(log_daño, True, self.c.BLANCO)
        ventana.blit(txt_log, (350, 40))

    def _barra_vida(self, ventana, x, y, actual, maximo, color, nombre):
        """Dibuja una barra de salud proporcional"""
        ancho_b = 220
        ratio = max(0, min(actual / maximo, 1))
        pygame.draw.rect(ventana, (60, 60, 60), (x, y, ancho_b, 25)) # Fondo gris
        pygame.draw.rect(ventana, color, (x, y, int(ancho_b * ratio), 25)) # Vida real
        info = self.c.f_chica.render(f"{nombre}: {actual}", True, self.c.BLANCO)
        ventana.blit(info, (x, y - 30))

    def dibujar_derrota(self, ventana, mensaje_sistema):
        """Pantalla de Game Over activada por jugador.vivo = False"""
        # Capa de oscuridad
        s = pygame.Surface((930, 600))
        s.set_alpha(210)
        s.fill((10, 0, 0))
        ventana.blit(s, (0, 0))

        # Mensaje "Te jalaste EDO"
        tit = self.c.f_grande.render("HAS PERDIDO", True, (255, 0, 0))
        msg = self.c.f_chica.render(mensaje_sistema, True, self.c.BLANCO)
        
        ventana.blit(tit, (320, 200))
        ventana.blit(msg, (310, 300))

        # Botón de Reinicio
        pygame.draw.rect(ventana, self.c.BLANCO, self.rect_boton_reinicio, border_radius=10)
        txt_btn = self.c.f_chica.render("REINTENTAR", True, self.c.NEGRO)
        ventana.blit(txt_btn, (self.rect_boton_reinicio.x + 45, self.rect_boton_reinicio.y + 12))