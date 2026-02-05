import pygame

# Esta clase dibuja el menu principal y la pantalla de seleccion de personajes
class Menu_Vista:
    def __init__(self, config):
        self.c = config

    def dibujar_menu(self, ventana, modelo):
        """
        Dibuja la pantalla de titulo con los botones de modo de juego.
        Se cambio el nombre manteniendo la posicion original.
        """
        try:
            # Carga el fondo desde la carpeta de recursos
            ruta = modelo.rutas.obtener_ruta_archivo("fondo.png") 
            img = pygame.image.load(ruta)
            img = pygame.transform.scale(img, (930, 600))
            ventana.blit(img, (0, 0))
        except:
            # Color de respaldo si falla la imagen
            ventana.fill((10, 10, 30))

        # 1. DIBUJO DEL TITULO 
        # El primer texto va en la posicion 350 de altura
        self._texto(ventana, "ECOS DE", 55, 350, True)
        # El segundo texto va en la posicion 400 de altura
        self._texto(ventana, "LA CARTA", 90, 400, True)
        
        # 2. BOTONES DE MODO DE JUEGO
        # Mantienen las coordenadas exactas para que el clic del controlador coincida
        self._boton(ventana, 50, 450, "1P")  # Boton para un jugador
        self._boton(ventana, 190, 450, "2P") # Boton para dos jugadores
        
    def dibujar_seleccion_clase(self, ventana, modelo):
        """Dibuja la galeria de personajes para que el usuario elija uno"""
        try:
            # Usa el fondo especial llamado Fondo_Elmo
            ruta_elmo = modelo.rutas.obtener_ruta_archivo("Fondo_Elmo.png")
            fondo = pygame.image.load(ruta_elmo)
            ventana.blit(pygame.transform.scale(fondo, (930, 600)), (0, 0))
        except:
            ventana.fill((20, 20, 20))

        # Titulo centrado usando la mitad del ancho de la ventana (930 / 2 = 465)
        titulo = self.c.f_grande.render("ELIGE TU DESTINO", True, self.c.NEON)
        ventana.blit(titulo, (465 - titulo.get_width()//2, 50))

        # Lista de las 4 clases disponibles
        clases = ["Fuego", "Agua", "Tierra", "Aire"]
        for i, nombre in enumerate(clases):
            x, y = 50 + (i * 220), 180
            
            # Intenta cargar la imagen del personaje nivel 1 para mostrarlo
            try:
                # Le pide al arbol de evolucion el nombre del nivel 1 (ej. 'Gota Joven')
                nombre_evo = modelo.evolucion.obtener_nombre_evolucion(nombre, 1)
                # Pide la ruta del archivo de esa evolucion
                ruta_pj = modelo.rutas.obtener_ruta_personaje(nombre, nombre_evo)
                img = pygame.image.load(ruta_pj)
                img = pygame.transform.scale(img, (180, 200))
                ventana.blit(img, (x, y))
            except:
                # Si no encuentra la foto, dibuja un cuadro gris
                pygame.draw.rect(ventana, (50, 50, 50), (x, y, 180, 200))
            
            # Dibuja el marco neon alrededor de cada opcion
            pygame.draw.rect(ventana, self.c.NEON, (x, y, 180, 200), 2, border_radius=5)
            
            # Pone el nombre del elemento en mayusculas debajo de la foto
            txt_clase = self.c.f_chica.render(nombre.upper(), True, self.c.BLANCO)
            ventana.blit(txt_clase, (x + 90 - txt_clase.get_width()//2, y + 210))

    def _texto(self, ventana, texto, x, y, sombra=False):
        """Metodo privado para escribir texto con o sin sombra"""
        if sombra:
            # Dibuja el mismo texto un poco desplazado en negro para el efecto de sombra
            s = self.c.f_grande.render(texto, True, self.c.NEGRO)
            ventana.blit(s, (x + 4, y + 4))
        t = self.c.f_grande.render(texto, True, self.c.BLANCO)
        ventana.blit(t, (x, y))

    def _boton(self, ventana, x, y, texto):
        """Metodo privado para dibujar botones estilizados con borde neon"""
        pygame.draw.rect(ventana, self.c.NEON, (x, y, 100, 50), 2, border_radius=10)
        
        # Intenta usar la fuente media, si no existe usa la chica por seguridad
        fuente = getattr(self.c, 'f_media', self.c.f_chica)
        
        t = fuente.render(texto, True, self.c.BLANCO)
        # Calcula el centro exacto del rectangulo para que el texto no quede chueco
        ventana.blit(t, (x + 50 - t.get_width()//2, y + 25 - t.get_height()//2))