import pygame
import math

class Combate_Vista:
    def __init__(self, config):
        self.c = config
        self.rect_boton_hab = pygame.Rect(350, 480, 230, 60)

    def dibujar_combate(self, ventana, modelo, log_daño):
        jugador = modelo.obtener_jugador_actual()
        
        # 1. FONDO DE COMBATE (El modelo decide si es Boss o Comedor)
        try:
            ruta_fondo = modelo.obtener_ruta_fondo_combate()
            fondo = pygame.image.load(ruta_fondo)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
            
            # Oscurecer un poco
            overlay = pygame.Surface((930, 600), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            ventana.blit(overlay, (0, 0))
        except:
            ventana.fill((30, 10, 10))

        # 2. PERSONAJES (Efecto flotante)
        tiempo = pygame.time.get_ticks() / 1000
        flotacion = math.sin(tiempo) * 10
        
        # --- JUGADOR ---
        try:
            ruta_pj = modelo.obtener_ruta_imagen_personaje()
            img_p = pygame.image.load(ruta_pj)
            img_p = pygame.transform.scale(img_p, (200, 260))
            ventana.blit(img_p, (100, 150 + flotacion))
            
            # Nombre Evolución
            nom_evo = modelo.info_visual()
            txt_p = self.c.f_chica.render(nom_evo, True, self.c.BLANCO)
            ventana.blit(txt_p, (100, 120 + flotacion))
        except:
            pygame.draw.rect(ventana, (0, 255, 0), (100, 150, 200, 260))

        # --- ENEMIGO ---
        # Nota: El enemigo no está 100% en el modelo aún, usamos búsqueda genérica
        # a través del gestor de rutas del modelo
        try:
            nodo = getattr(jugador, "nodo_actual", "")
            nombre_enemigo = "Boss_Final.png" if nodo == "Piso 5" else "Enemigo.png"
            
            # Usamos el gestor de rutas para buscar la imagen del enemigo
            # (Truco: le pasamos el nombre del archivo como si fuera una evolución para que lo busque)
            ruta_e = modelo.rutas.obtener_ruta_personaje("Enemigo", nombre_enemigo)
            
            img_e = pygame.image.load(ruta_e)
            img_e = pygame.transform.scale(img_e, (200, 260))
            ventana.blit(img_e, (630, 150 - flotacion))
        except:
            pygame.draw.rect(ventana, (255, 0, 0), (630, 150, 200, 260))

        # 3. INTERFAZ (Barras y Botón)
        # Necesitamos el objeto enemigo para la barra (lo pasamos en log o lo sacamos de algun lado)
        # Como este metodo recibe (ventana, modelo, log), asumimos que el controlador maneja la logica.
        # PERO: Para dibujar la vida del enemigo, normalmente necesitamos el objeto enemigo.
        # Si no lo tenemos aqui, dibujaremos placeholder o necesitariamos pasarlo.
        # *Asumiré que NO cambiamos la firma, pero mostraré barras genéricas si falta datos*
        
        # Barra Jugador
        self._barra_vida(ventana, 100, 450, jugador.vidas, 5, (0, 255, 0), "TU VIDA")
        
        # Botón Ataque
        pygame.draw.rect(ventana, self.c.NEON, self.rect_boton_hab, border_radius=10)
        hab_actual = getattr(jugador, "habilidad_actual", "Ataque")
        txt_btn = self.c.f_chica.render(f"ATACAR: {hab_actual}", True, self.c.NEGRO)
        ventana.blit(txt_btn, txt_btn.get_rect(center=self.rect_boton_hab.center))

        # Log
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