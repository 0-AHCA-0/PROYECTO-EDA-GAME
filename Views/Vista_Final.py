import pygame

class Vista_Final:
    def __init__(self, config):
        self.c = config
        # Boton centrado para finalizar la partida
        self.rect_boton_fin = pygame.Rect(315, 420, 300, 65)

    def dibujar_victoria(self, ventana, modelo):
        """Pantalla de celebracion al aprobar el proyecto final"""
        # 1. Capa de exito (Verde oscuro transparente)
        overlay = pygame.Surface((930, 600), pygame.SRCALPHA)
        overlay.fill((0, 30, 0, 215)) 
        ventana.blit(overlay, (0, 0))

        jugador = modelo.obtener_jugador_actual()
        if not jugador: return

        # 2. Titulo de victoria
        txt_titulo = "¡PROYECTO APROBADO!"
        color_victoria = (0, 255, 150) # Verde esmeralda
        
        # Sombra
        sombra = self.c.f_grande.render(txt_titulo, True, (0, 0, 0))
        ventana.blit(sombra, ((930 - sombra.get_width()) // 2 + 3, 153))
        
        frente = self.c.f_grande.render(txt_titulo, True, color_victoria)
        ventana.blit(frente, ((930 - frente.get_width()) // 2, 150))

        # 3. Mensaje de Logro Academico
        mensaje = f"Felicidades {jugador.nombre}. Has aprobado EDA y vencido a Boris."
        txt_msg = self.c.f_chica.render(mensaje, True, (255, 255, 255))
        ventana.blit(txt_msg, (465 - txt_msg.get_width()//2, 260))

        txt_sub = self.c.f_chica.render("Tu cupo ha terminado con éxito.", True, (200, 200, 200))
        ventana.blit(txt_sub, (465 - txt_sub.get_width()//2, 300))

        # 4. Boton para volver al Menu
        pygame.draw.rect(ventana, (20, 20, 20), self.rect_boton_fin, border_radius=12)
        pygame.draw.rect(ventana, color_victoria, self.rect_boton_fin, 3, border_radius=12)
        
        txt_btn = self.c.f_chica.render("VOLVER AL MENU", True, (255, 255, 255))
        ventana.blit(txt_btn, (self.rect_boton_fin.centerx - txt_btn.get_width()//2, 
                            self.rect_boton_fin.centery - txt_btn.get_height()//2))