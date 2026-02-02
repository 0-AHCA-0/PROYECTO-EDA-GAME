import pygame
import math

class Combate_Vista:
    def __init__(self, config):
        self.c = config
        self.rect_boton_hab = pygame.Rect(350, 480, 230, 60)

    def dibujar_combate(self, ventana, modelo, log_daño):
        jugador = modelo.obtener_jugador_actual()
        if not jugador: return

        # 1. FONDO DE COMBATE (Mantengo tu lógica intacta)
        try:
            ruta_fondo = modelo.obtener_ruta_fondo_combate()
            fondo = pygame.image.load(ruta_fondo)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
            overlay = pygame.Surface((930, 600), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            ventana.blit(overlay, (0, 0))
        except:
            ventana.fill((30, 10, 10))

        # 2. PERSONAJES (Efecto flotante - Mantengo tu lógica)
        tiempo = pygame.time.get_ticks() / 1000
        flotacion = math.sin(tiempo) * 10
        
        # Jugador
        try:
            ruta_pj = modelo.obtener_ruta_imagen_personaje()
            img_p = pygame.image.load(ruta_pj)
            img_p = pygame.transform.scale(img_p, (200, 260))
            ventana.blit(img_p, (100, 150 + flotacion))
            nom_evo = modelo.info_visual()
            txt_p = self.c.f_chica.render(nom_evo, True, self.c.BLANCO)
            ventana.blit(txt_p, (100, 120 + flotacion))
        except:
            pygame.draw.rect(ventana, (0, 255, 0), (100, 150, 200, 260))

        # Enemigo
        try:
            nodo = getattr(jugador, "nodo_actual", "")
            nombre_enemigo = "Boris.png" if nodo == "Piso 5" else "Enemigo.png"
            ruta_e = modelo.rutas.obtener_ruta_personaje("Enemigo", nombre_enemigo)
            img_e = pygame.image.load(ruta_e)
            img_e = pygame.transform.scale(img_e, (200, 260))
            ventana.blit(img_e, (630, 150 - flotacion))
        except:
            pygame.draw.rect(ventana, (255, 0, 0), (630, 150, 200, 260))

        # ---------------------------------------------------------
        # 3. INTERFAZ SINCRONIZADA (AQUÍ ESTÁ EL CAMBIO)
        # ---------------------------------------------------------
        
        # BARRA DE VIDA JUGADOR (LPs)
        x_bar, y_bar = 100, 450
        ancho_max = 250
        # Calculamos el porcentaje de la barra (ej: 100/100 = 100%)
        porcentaje = max(0, jugador.vida / jugador.vida_max)
        
        # Dibujar barra fondo y barra salud
        pygame.draw.rect(ventana, (40, 40, 40), (x_bar, y_bar, ancho_max, 25)) # Fondo
        color_barra = self.c.NEON if porcentaje > 0.3 else (255, 50, 50)
        pygame.draw.rect(ventana, color_barra, (x_bar, y_bar, int(ancho_max * porcentaje), 25))
        
        # TEXTO DE LPs (Mostrará 100 LP, 85 LP, etc.)
        txt_lp = self.c.f_chica.render(f"LP: {int(jugador.vida)} / {jugador.vida_max}", True, self.c.BLANCO)
        ventana.blit(txt_lp, (x_bar, y_bar - 30))

        # INDICADOR DE VIDAS GLOBALES (Los corazones/bolitas al lado)
        for i in range(jugador.vidas):
            pygame.draw.circle(ventana, (255, 0, 0), (x_bar + ancho_max + 30 + (i * 20), y_bar + 12), 8)

        # BOTÓN ATAQUE
        pygame.draw.rect(ventana, self.c.NEON, self.rect_boton_hab, border_radius=10)
        hab_actual = getattr(jugador, "habilidad_actual", "Ataque")
        txt_btn = self.c.f_chica.render(f"ATACAR: {hab_actual}", True, self.c.NEGRO)
        ventana.blit(txt_btn, txt_btn.get_rect(center=self.rect_boton_hab.center))

        # LOG DE COMBATE
        s = pygame.Surface((600, 40))
        s.set_alpha(150); s.fill((0,0,0))
        ventana.blit(s, (165, 30))
        txt_log = self.c.f_chica.render(log_daño, True, self.c.BLANCO)
        ventana.blit(txt_log, (465 - txt_log.get_width()//2, 40))

    def dibujar_enemigo_vida(self, ventana, enemigo):
        """Helper extra si tienes el objeto enemigo a mano"""
        vida = getattr(enemigo, "vida", getattr(enemigo, "hp", 0))
        max_vida = getattr(enemigo, "vidas_max", 100)
        self._barra_vida(ventana, 630, 450, vida, max_vida, (255, 0, 0), "ENEMIGO")

    def _barra_vida(self, ventana, x, y, actual, maximo, color, nombre):
        ancho = 200
        if maximo <= 0: maximo = 1
        ratio = max(0, min(actual / maximo, 1))
        pygame.draw.rect(ventana, (50, 50, 50), (x, y, ancho, 20), border_radius=5)
        if ratio > 0: pygame.draw.rect(ventana, color, (x, y, int(ancho * ratio), 20), border_radius=5)
        ventana.blit(self.c.f_chica.render(f"{nombre}: {actual}", True, self.c.BLANCO), (x, y - 25))

    def dibujar_derrota(self, ventana, msj):
        s = pygame.Surface((930, 600), pygame.SRCALPHA); s.fill((0,0,0,200))
        ventana.blit(s, (0,0))
        txt = self.c.f_grande.render("GAME OVER", True, (255, 0, 0))
        ventana.blit(txt, txt.get_rect(center=(465, 300)))