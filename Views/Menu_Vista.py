import pygame

class Menu_Vista:
    def __init__(self, config):
        self.c = config

    def dibujar_menu(self, ventana, modelo):
        try:
            ruta = modelo.rutas.obtener_ruta_archivo("fondo.png") 
            img = pygame.image.load(ruta)
            img = pygame.transform.scale(img, (930, 600))
            ventana.blit(img, (0, 0))
        except:
            ventana.fill((10, 10, 30))

        self._texto(ventana, "LEYENDAS", 90, 350, True)
        self._texto(ventana, "ELEMENTALES", 53, 400, True)
        self._boton(ventana, 50, 450, "1P")
        self._boton(ventana, 190, 450, "2P")

    def dibujar_seleccion_clase(self, ventana, modelo):
        try:
            # USANDO EL NOMBRE EXACTO: Fondo_Elmo
            ruta_elmo = modelo.rutas.obtener_ruta_archivo("Fondo_Elmo.png")
            fondo = pygame.image.load(ruta_elmo)
            ventana.blit(pygame.transform.scale(fondo, (930, 600)), (0, 0))
        except:
            ventana.fill((20, 20, 20))

        titulo = self.c.f_grande.render("ELIGE TU DESTINO", True, self.c.NEON)
        ventana.blit(titulo, (465 - titulo.get_width()//2, 50))

        clases = ["Fuego", "Agua", "Tierra", "Aire"]
        for i, nombre in enumerate(clases):
            x, y = 50 + (i * 220), 180
            
            # Imagen del personaje nivel 1 desde el ArbolEvolucion
            try:
                nombre_evo = modelo.evolucion.obtener_nombre_evolucion(nombre, 1)
                ruta_pj = modelo.rutas.obtener_ruta_personaje(nombre, nombre_evo)
                img = pygame.image.load(ruta_pj)
                img = pygame.transform.scale(img, (180, 200))
                ventana.blit(img, (x, y))
            except:
                pygame.draw.rect(ventana, (50, 50, 50), (x, y, 180, 200))
            
            # Marco de selección
            pygame.draw.rect(ventana, self.c.NEON, (x, y, 180, 200), 2, border_radius=5)
            
            # NOMBRE DE CLASE REAL (No genérico)
            txt_clase = self.c.f_chica.render(nombre.upper(), True, self.c.BLANCO)
            ventana.blit(txt_clase, (x + 90 - txt_clase.get_width()//2, y + 210))

    def _texto(self, ventana, texto, x, y, sombra=False):
        if sombra:
            s = self.c.f_grande.render(texto, True, self.c.NEGRO)
            ventana.blit(s, (x + 4, y + 4))
        t = self.c.f_grande.render(texto, True, self.c.BLANCO)
        ventana.blit(t, (x, y))

    def _boton(self, ventana, x, y, texto):
        pygame.draw.rect(ventana, self.c.NEON, (x, y, 100, 50), 2, border_radius=10)
        
        # Intentamos usar f_media, si falla usamos f_chica por defecto
        fuente = getattr(self.c, 'f_media', self.c.f_chica)
        
        t = fuente.render(texto, True, self.c.BLANCO)
        ventana.blit(t, (x + 50 - t.get_width()//2, y + 25 - t.get_height()//2))