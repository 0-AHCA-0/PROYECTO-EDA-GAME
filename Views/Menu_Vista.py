import pygame
import os

class Menu_Vista:
    def __init__(self, config):
        """Recibe la configuración de colores y fuentes"""
        self.c = config
        self.ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def dibujar_menu(self, ventana):
        # 1. DIBUJAR EL FONDO
        try:
            ruta_fondo = os.path.join(self.ruta_proyecto, "Imagenes", "fondo.png")
            fondo = pygame.image.load(ruta_fondo)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
        except Exception as e:
            print(f"Error al cargar fondo.png: {e}")
            ventana.fill((20, 20, 40))

        # 2. EL TÍTULO (Renderizado con sombras)
        # Línea 1: LEYENDAS
        render_1 = self.c.f_grande.render("LEYENDAS", True, self.c.BLANCO)
        sombra_1 = self.c.f_grande.render("LEYENDAS", True, self.c.NEGRO)
        ventana.blit(sombra_1, (90, 350)) 
        ventana.blit(render_1, (87, 347)) 

        # Línea 2: ELEMENTALES
        render_2 = self.c.f_grande.render("ELEMENTALES", True, self.c.BLANCO)
        sombra_2 = self.c.f_grande.render("ELEMENTALES", True, self.c.NEGRO)
        ventana.blit(sombra_2, (53, 400)) 
        ventana.blit(render_2, (50, 397))

        # 3. LOS BOTONES (P1 y P2)
        # Botón P1
        rect_p1 = pygame.Rect(50, 450, 100, 50)
        pygame.draw.rect(ventana, self.c.NEGRO, (48, 448, 104, 54), border_radius=15)
        pygame.draw.rect(ventana, self.c.BLANCO, rect_p1, border_radius=15)
        txt_p1 = self.c.f_chica.render("1P", True, self.c.NEGRO)
        ventana.blit(txt_p1, (90, 465))

        # Botón P2
        rect_p2 = pygame.Rect(190, 450, 100, 50)
        pygame.draw.rect(ventana, self.c.NEGRO, (188, 448, 104, 54), border_radius=15)
        pygame.draw.rect(ventana, self.c.BLANCO, rect_p2, border_radius=15)
        txt_p2 = self.c.f_chica.render("2P", True, self.c.NEGRO)
        ventana.blit(txt_p2, (230, 465))
        
        # TEXTO INFORMATIVO
        info = self.c.f_chica.render("P1: Solo      P2: Versus", True, self.c.BLANCO)
        pygame.draw.rect(ventana, (0,0,0), (50, 510, 250, 30)) 
        ventana.blit(info, (55, 515))

    def dibujar_seleccion_clase(self, ventana):
        # 1. DIBUJAR EL FONDO
        try:
            ruta_fondo = os.path.join(self.ruta_proyecto, "Imagenes", "Fondo_Elmo.png")
            fondo = pygame.image.load(ruta_fondo)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
        except Exception as e:
            print(f"Error al cargar fondo_seleccion.png: {e}")
            ventana.fill(self.c.NEGRO)
        
        # 2. TÍTULO
        texto = self.c.f_grande.render("Elige Clase:", True, self.c.BLANCO)
        ventana.blit(texto, (100, 50))
                
        # 3. CARGAR Y MOSTRAR LAS 4 CLASES
        clases_info = {
            "Agua": "P_Agua.png", "Tierra": "P_Tierra.png",
            "Fuego": "P_Fuego.png", "Aire": "P_Aire.png"
        }
        
        clases = list(clases_info.keys())
        espacio_x = 220 
        y_inicio = 180   
        x_inicio = 50    
        
        for i, clase in enumerate(clases):
            x_pos = x_inicio + (i * espacio_x)
            try:
                # Carga de imagen dinámica
                ruta_img = os.path.join(self.ruta_proyecto, "Imagenes", clases_info[clase])
                imagen = pygame.image.load(ruta_img)
                imagen = pygame.transform.scale(imagen, (180, 200))
                ventana.blit(imagen, (x_pos, y_inicio))
                pygame.draw.rect(ventana, self.c.BLANCO, (x_pos, y_inicio, 181, 201), 5)
            except:
                pygame.draw.rect(ventana, (100, 100, 100), (x_pos, y_inicio, 180, 200))
            
            # Etiqueta debajo de la imagen
            etiqueta = self.c.f_grande.render(clase, True, self.c.BLANCO) # Deysi usó f_etiqueta aquí
            rect_etiqueta = etiqueta.get_rect(topleft=(x_pos + 30, y_inicio + 250))
            pygame.draw.rect(ventana, self.c.NEGRO, rect_etiqueta.inflate(20, 10), border_radius=8)
            ventana.blit(etiqueta, (x_pos + 30, y_inicio + 250))