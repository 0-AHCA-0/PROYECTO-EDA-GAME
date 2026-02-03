import pygame
import math

class Combate_Vista:
    def __init__(self, config):
        self.c = config
        # Boton centrado
        self.rect_boton_hab = pygame.Rect(350, 480, 230, 60)

    def dibujar_combate(self, ventana, modelo, log_daño):
        jugador = modelo.obtener_jugador_actual()
        if not jugador: return

        # 1. FONDO
        try:
            ruta_fondo = modelo.obtener_ruta_fondo_combate()
            fondo = pygame.image.load(ruta_fondo)
            ventana.blit(pygame.transform.scale(fondo, (930, 600)), (0, 0))
            overlay = pygame.Surface((930, 600), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 110))
            ventana.blit(overlay, (0, 0))
        except:
            ventana.fill((20, 20, 20))

        # 2. PERSONAJES
        t = pygame.time.get_ticks() / 1000
        mov = math.sin(t) * 10
        
        # Jugador
        try:
            img_p = pygame.image.load(modelo.obtener_ruta_imagen_personaje())
            ventana.blit(pygame.transform.scale(img_p, (200, 260)), (100, 150 + mov))
            txt_p = self.c.f_chica.render(modelo.info_visual(), True, self.c.BLANCO)
            ventana.blit(txt_p, (100, 120 + mov))
        except:
            pygame.draw.rect(ventana, (0, 200, 0), (100, 150, 200, 260), 2)

        # Enemigo
        enemigo = modelo.encuentros.enemigo_actual
        if enemigo:
            try:
                # Ajuste de nombre de imagen segun nodo
                nodo = getattr(jugador, "nodo_actual", "Campus")
                nombre_img = "Boris.png" if nodo == "Piso 5" else "Enemigo.png"
                ruta_e = modelo.rutas.obtener_ruta_personaje("Enemigo", nombre_img)
                img_e = pygame.image.load(ruta_e)
                
                # Nombre sobre el enemigo
                txt_nom_e = self.c.f_chica.render(enemigo.nombre.upper(), True, (255, 100, 100))
                ventana.blit(txt_nom_e, (730 - txt_nom_e.get_width()//2, 120 - mov))
                ventana.blit(pygame.transform.scale(img_e, (200, 260)), (630, 150 - mov))
            except:
                pygame.draw.rect(ventana, (255, 0, 0), (630, 150, 200, 260), 2)

        # 3. INTERFAZ (Letra compacta tipo Arial)
        x_bar, y_bar = 100, 450
        
        # Vida Jugador
        self._barra_vida(ventana, x_bar, y_bar, jugador.vida, jugador.vida_max, self.c.NEON, "LP")
        
        # --- VIDAS GLOBALES: DEBAJO DE LOS LP ---
        for i in range(jugador.vidas):
            pygame.draw.circle(ventana, (255, 40, 40), (x_bar + (i * 18), y_bar + 25), 6)

        # Vida Enemigo
        if enemigo:
            v_max_e = getattr(enemigo, "vida_max", 100)
            self._barra_vida(ventana, 630, y_bar, enemigo.vida, v_max_e, (255, 50, 50), enemigo.nombre.upper())

        # BOTON ATAQUE (Uso de get_rect para centrar sin estirar)
        pygame.draw.rect(ventana, (10, 10, 10), self.rect_boton_hab, border_radius=10)
        pygame.draw.rect(ventana, self.c.NEON, self.rect_boton_hab, 2, border_radius=10)
        
        hab = getattr(jugador, "habilidad_actual", "Ataque")
        txt_btn = self.c.f_chica.render(f"USAR: {hab.upper()}", True, self.c.BLANCO)
        ventana.blit(txt_btn, txt_btn.get_rect(center=self.rect_boton_hab.center))

        # LOG SUPERIOR
        txt_l = self.c.f_chica.render(log_daño, True, self.c.BLANCO)
        ventana.blit(txt_l, (465 - txt_l.get_width()//2, 40))

    def _barra_vida(self, ventana, x, y, actual, maximo, color, nombre):
        ancho = 200
        ratio = max(0, min(actual / (maximo if maximo > 0 else 1), 1))
        pygame.draw.rect(ventana, (40, 40, 40), (x, y, ancho, 12), border_radius=4)
        if ratio > 0:
            pygame.draw.rect(ventana, color, (x, y, int(ancho * ratio), 12), border_radius=4)
        
        txt_val = self.c.f_chica.render(f"{nombre}: {int(actual)}", True, self.c.BLANCO)
        ventana.blit(txt_val, (x, y - 22))

    def dibujar_derrota(self, ventana, msj):
        s = pygame.Surface((930, 600), pygame.SRCALPHA); s.fill((0, 0, 0, 220))
        ventana.blit(s, (0, 0))
        txt = self.c.f_grande.render("DERROTA", True, (255, 0, 0))
        ventana.blit(txt, txt.get_rect(center=(465, 300)))