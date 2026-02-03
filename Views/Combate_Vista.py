import pygame
import math

class Combate_Vista:
    def __init__(self, config):
        self.c = config
        # Botón centrado en la parte inferior
        self.rect_boton_hab = pygame.Rect(350, 480, 230, 60)

    def dibujar_combate(self, ventana, modelo, log_daño):
        jugador = modelo.obtener_jugador_actual()
        if not jugador: return

        # 1. FONDO DE COMBATE
        try:
            ruta_fondo = modelo.obtener_ruta_fondo_combate()
            fondo = pygame.image.load(ruta_fondo)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
            
            # Capa de oscurecimiento para resaltar la UI
            overlay = pygame.Surface((930, 600), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            ventana.blit(overlay, (0, 0))
        except:
            ventana.fill((30, 10, 10))

        # 2. PERSONAJES (Efecto flotante)
        tiempo = pygame.time.get_ticks() / 1000
        flotacion = math.sin(tiempo) * 10
        
        # --- Dibujar Jugador ---
        try:
            ruta_pj = modelo.obtener_ruta_imagen_personaje()
            img_p = pygame.image.load(ruta_pj)
            img_p = pygame.transform.scale(img_p, (200, 260))
            ventana.blit(img_p, (100, 150 + flotacion))
            
            nom_evo = modelo.info_visual()
            txt_p = self.c.f_chica.render(nom_evo, True, self.c.BLANCO)
            ventana.blit(txt_p, (100, 120 + flotacion))
        except:
            pygame.draw.rect(ventana, (0, 255, 0), (100, 150, 200, 260), 2)

        # --- Dibujar Enemigo ---
        enemigo = modelo.encuentros.enemigo_actual
        try:
            nodo = getattr(jugador, "nodo_actual", "Campus")
            # Si es el jefe final en Piso 5 usamos Boris, si no, Enemigo genérico
            nombre_img_enemigo = "Boris.png" if nodo == "Piso 5" else "Enemigo.png"
            ruta_e = modelo.rutas.obtener_ruta_personaje("Enemigo", nombre_img_enemigo)
            img_e = pygame.image.load(ruta_e)
            img_e = pygame.transform.scale(img_e, (200, 260))
            ventana.blit(img_e, (630, 150 - flotacion))
        except:
            pygame.draw.rect(ventana, (255, 0, 0), (630, 150, 200, 260), 2)

        # ---------------------------------------------------------
        # 3. INTERFAZ DE VIDA Y BOTONES
        # ---------------------------------------------------------
        
        # VIDA DEL JUGADOR (Lado Izquierdo)
        self._barra_vida(ventana, 100, 450, jugador.vida, jugador.vida_max, self.c.NEON, "JUGADOR")
        
        # INDICADOR DE VIDAS GLOBALES (Corazones)
        for i in range(jugador.vidas):
            pygame.draw.circle(ventana, (255, 50, 50), (100 + (i * 25), 420), 8)

        # VIDA DEL ENEMIGO (Lado Derecho)
        if enemigo:
            # Usamos vida_max del enemigo definida en el controlador
            v_max_e = getattr(enemigo, "vida_max", 100)
            self._barra_vida(ventana, 630, 450, enemigo.vida, v_max_e, (255, 50, 50), "ENEMIGO")

        # BOTÓN ATAQUE
        pygame.draw.rect(ventana, self.c.NEON, self.rect_boton_hab, border_radius=10)
        hab_actual = getattr(jugador, "habilidad_actual", "Ataque")
        txt_btn = self.c.f_chica.render(f"USAR: {hab_actual}", True, self.c.NEGRO)
        ventana.blit(txt_btn, txt_btn.get_rect(center=self.rect_boton_hab.center))

        # LOG DE COMBATE (Caja de texto superior)
        s_log = pygame.Surface((600, 40))
        s_log.set_alpha(180)
        s_log.fill((20, 20, 20))
        ventana.blit(s_log, (165, 30))
        txt_log = self.c.f_chica.render(log_daño, True, self.c.BLANCO)
        ventana.blit(txt_log, (465 - txt_log.get_width()//2, 40))

    def _barra_vida(self, ventana, x, y, actual, maximo, color, nombre):
        """Dibuja una barra de salud estandarizada con fondo y borde."""
        ancho_total = 200
        # Evitar división por cero
        if maximo <= 0: maximo = 1
        ratio = max(0, min(actual / maximo, 1))
        
        # Fondo oscuro de la barra
        pygame.draw.rect(ventana, (40, 40, 40), (x, y, ancho_total, 20), border_radius=5)
        # Parte llena
        if ratio > 0:
            pygame.draw.rect(ventana, color, (x, y, int(ancho_total * ratio), 20), border_radius=5)
        # Borde
        pygame.draw.rect(ventana, self.c.BLANCO, (x, y, ancho_total, 20), 1, border_radius=5)
        
        # Texto con valores numéricos
        txt_val = self.c.f_chica.render(f"{nombre}: {int(actual)}/{int(maximo)}", True, self.c.BLANCO)
        ventana.blit(txt_val, (x, y - 25))

    def dibujar_derrota(self, ventana, msj):
        """Pantalla de Game Over"""
        overlay = pygame.Surface((930, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        ventana.blit(overlay, (0, 0))
        
        txt_main = self.c.f_grande.render("DERROTA", True, (255, 0, 0))
        txt_sub = self.c.f_chica.render(msj, True, self.c.BLANCO)
        
        ventana.blit(txt_main, txt_main.get_rect(center=(465, 280)))
        ventana.blit(txt_sub, txt_sub.get_rect(center=(465, 340)))