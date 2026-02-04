import pygame

# Esta clase muestra la pantalla de victoria cuando el jugador gana el juego
class Vista_Final:
    def __init__(self, config):
        self.c = config
        # Area del boton para regresar al menu principal tras ganar
        self.rect_boton_fin = pygame.Rect(315, 420, 300, 65)

    def dibujar_victoria(self, ventana, modelo):
        """Dibuja la pantalla de celebracion con el mensaje de exito"""
        # 1. CAPA DE EXITO
        # Crea un filtro verde oscuro transparente para cubrir el juego de fondo
        overlay = pygame.Surface((930, 600), pygame.SRCALPHA)
        overlay.fill((0, 30, 0, 215)) 
        ventana.blit(overlay, (0, 0))

        jugador = modelo.obtener_jugador_actual()
        if not jugador: return

        # 2. TITULO DE VICTORIA
        txt_titulo = "¡PROYECTO APROBADO!"
        color_victoria = (0, 255, 150) # Color verde esmeralda brillante
        
        # Dibuja una sombra negra desplazada 3 pixeles para que el titulo resalte
        sombra = self.c.f_grande.render(txt_titulo, True, (0, 0, 0))
        ventana.blit(sombra, ((930 - sombra.get_width()) // 2 + 3, 153))
        
        # Dibuja el texto principal centrado
        frente = self.c.f_grande.render(txt_titulo, True, color_victoria)
        ventana.blit(frente, ((930 - frente.get_width()) // 2, 150))

        # 3. MENSAJES PERSONALIZADOS
        # Felicita al jugador por su nombre y menciona la victoria sobre Boris
        mensaje = f"Felicidades {jugador.nombre}. Has aprobado EDA y vencido a Boris."
        txt_msg = self.c.f_chica.render(mensaje, True, (255, 255, 255))
        ventana.blit(txt_msg, (465 - txt_msg.get_width()//2, 260))

        # Subtitulo tematico sobre el fin del ciclo academico
        txt_sub = self.c.f_chica.render("Tu cupo ha terminado con éxito.", True, (200, 200, 200))
        ventana.blit(txt_sub, (465 - txt_sub.get_width()//2, 300))

        # 4. BOTON DE CIERRE
        # Dibuja el rectangulo del boton con un borde del mismo color verde
        pygame.draw.rect(ventana, (20, 20, 20), self.rect_boton_fin, border_radius=12)
        pygame.draw.rect(ventana, color_victoria, self.rect_boton_fin, 3, border_radius=12)
        
        # Centra el texto 'VOLVER AL MENU' dentro del rectangulo del boton
        txt_btn = self.c.f_chica.render("VOLVER AL MENU", True, (255, 255, 255))
        ventana.blit(txt_btn, (self.rect_boton_fin.centerx - txt_btn.get_width()//2, 
                            self.rect_boton_fin.centery - txt_btn.get_height()//2))