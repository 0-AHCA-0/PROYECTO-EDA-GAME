import pygame

class Menu_Vista:
    def __init__(self, config):
        self.c = config

    def dibujar_menu(self, ventana, modelo):
        # -----------------------------------------------------------
        # CAMBIO 1: Usamos 'obtener_ruta_archivo' con "fondo.png"
        # -----------------------------------------------------------
        try:
            # Aquí pedimos el archivo directo, sin pasar por el diccionario de nodos
            ruta = modelo.rutas.obtener_ruta_archivo("fondo.png") 
            fondo = pygame.image.load(ruta)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
        except Exception as e:
            print(f"Error cargando fondo menú: {e}")
            ventana.fill((20, 20, 40))

        # TÍTULO (Leyendas Elementales)
        self._dibujar_texto_sombra(ventana, "LEYENDAS", 90, 350)
        self._dibujar_texto_sombra(ventana, "ELEMENTALES", 53, 400)

        # BOTONES P1 / P2
        self._dibujar_boton(ventana, 50, 450, "1P")
        self._dibujar_boton(ventana, 190, 450, "2P")
        
        # Info
        info = self.c.f_chica.render("P1: Solo      P2: Versus", True, self.c.BLANCO)
        pygame.draw.rect(ventana, (0,0,0), (50, 510, 250, 30))
        ventana.blit(info, (55, 515))

    def dibujar_seleccion_clase(self, ventana, modelo):
        # -----------------------------------------------------------
        # CAMBIO 2: Usamos "Fondo_Elmo.png"
        # -----------------------------------------------------------
        try:
            ruta = modelo.rutas.obtener_ruta_archivo("Fondo_Elmo.png")
            fondo = pygame.image.load(ruta)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
        except:
            ventana.fill(self.c.NEGRO)
        
        texto = self.c.f_grande.render("Elige tu Elemento:", True, self.c.BLANCO)
        ventana.blit(texto, (100, 50))
                
        # --- CARGA DINÁMICA DE CLASES ---
        clases = ["Fuego", "Agua", "Tierra", "Aire"]
        x_inicio = 50
        
        for i, clase in enumerate(clases):
            x_pos = x_inicio + (i * 220)
            y_pos = 180
            
            # 1. Obtener nombre Nivel 1 (ej: "Aprendiz Hot")
            nombre_lv1 = modelo.evolucion.obtener_nombre_evolucion(clase, 1)
            
            # 2. Obtener ruta imagen
            try:
                ruta_img = modelo.rutas.obtener_ruta_personaje(clase, nombre_lv1)
                imagen = pygame.image.load(ruta_img)
                imagen = pygame.transform.scale(imagen, (180, 200))
                ventana.blit(imagen, (x_pos, y_pos))
                
                # Marco blanco simple
                pygame.draw.rect(ventana, self.c.BLANCO, (x_pos, y_pos, 181, 201), 5)
            except:
                pygame.draw.rect(ventana, (60, 60, 60), (x_pos, y_pos, 180, 200))

            # 3. Etiqueta con nombre
            etiqueta = self.c.f_chica.render(nombre_lv1, True, self.c.BLANCO)
            rect_etiqueta = etiqueta.get_rect(center=(x_pos + 90, y_pos + 230))
            bg_etiqueta = rect_etiqueta.inflate(20, 10)
            
            pygame.draw.rect(ventana, self.c.NEGRO, bg_etiqueta, border_radius=8)
            pygame.draw.rect(ventana, self.c.NEON, bg_etiqueta, 2, border_radius=8)
            ventana.blit(etiqueta, rect_etiqueta)

    # Helpers
    def _dibujar_texto_sombra(self, ventana, texto, x, y):
        sombra = self.c.f_grande.render(texto, True, self.c.NEGRO)
        frente = self.c.f_grande.render(texto, True, self.c.BLANCO)
        ventana.blit(sombra, (x+3, y+3))
        ventana.blit(frente, (x, y))

    def _dibujar_boton(self, ventana, x, y, texto):
        rect = pygame.Rect(x, y, 100, 50)
        pygame.draw.rect(ventana, self.c.NEGRO, (x-2, y-2, 104, 54), border_radius=15)
        pygame.draw.rect(ventana, self.c.BLANCO, rect, border_radius=15)
        txt = self.c.f_chica.render(texto, True, self.c.NEGRO)
        ventana.blit(txt, (x+40, y+15))