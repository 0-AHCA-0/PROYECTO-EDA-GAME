import pygame
import math
import os

class VistaJuego:
    def __init__(self):
        pygame.init()
        
        # --- OBTENER LA RUTA RAÍZ DEL PROYECTO ---
        # Esto funciona sin importar desde dónde ejecutes el script
        self.ruta_proyecto = os.path.dirname(os.path.abspath(__file__))
        
        # --- 1. DEFINIR TODOS LOS COLORES ---
        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
        self.ROJO = (200, 50, 50)  
        self.AZUL = (50, 50, 200)
        
        # --- 2. CARGA DE FUENTE PERSONALIZADA ---
        try:
            # Rutas absolutas usando la carpeta del script
            ruta_fuente = os.path.join(self.ruta_proyecto, "Fuentes", "Tipo1.ttf")
            ruta_fuente2 = os.path.join(self.ruta_proyecto, "Fuentes", "Tipo2.ttf")
            self.fuente_grande = pygame.font.Font(ruta_fuente, 50)
            self.fuente_etiqueta = pygame.font.Font(ruta_fuente, 60)  # Etiqueta de clases
            self.fuente_chica = pygame.font.Font(ruta_fuente2, 20)  
        except:
            print("No se encontró la fuente, usando Arial por defecto")
            self.fuente_grande = pygame.font.SysFont("Arial", 70, bold=True)
            self.fuente_etiqueta = pygame.font.SysFont("Arial", 36, bold=True)
            self.fuente_chica = pygame.font.SysFont("Arial", 24)

    def dibujar_menu(self, ventana):
        # 1. DIBUJAR EL FONDO
        try:
            # Ruta absoluta usando la carpeta del proyecto
            ruta_fondo = os.path.join(self.ruta_proyecto, "Imagenes", "fondo.png")
            fondo = pygame.image.load(ruta_fondo)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
        except Exception as e:
            # Si falla la imagen, usa fondo azul oscuro
            print(f"Error al cargar fondo.png: {e}")
            ventana.fill((20, 20, 40))

        # 2. EL TÍTULO (En dos líneas)
        
        # --- LÍNEA 1: "LEYENDAS" ---
        txt_1 = "LEYENDAS"
        render_1 = self.fuente_grande.render(txt_1, True, self.BLANCO)
        sombra_1 = self.fuente_grande.render(txt_1, True, self.NEGRO)
        
        # Las dibujamos arriba (ej. altura Y = 50)
        ventana.blit(sombra_1, (90, 350)) # Sombra
        ventana.blit(render_1, (87, 347)) # Texto

        # --- LÍNEA 2: "ELEMENTALES" ---
        txt_2 = "ELEMENTALES"
        render_2 = self.fuente_grande.render(txt_2, True, self.BLANCO)
        sombra_2 = self.fuente_grande.render(txt_2, True, self.NEGRO)
        
        # Las dibujamos más abajo (ej. altura Y = 110)
        # Sumamos 60 píxeles para que no se monten encima
        ventana.blit(sombra_2, (53, 400)) 
        ventana.blit(render_2, (50, 397))

        # 3. LOS BOTONES (P1 y P2)
        # --- Botón P1 ---
        rect_p1 = pygame.Rect(50, 450, 100, 50)
        # Borde negro para que resalte
        pygame.draw.rect(ventana, self.NEGRO, (48, 448, 104, 54), border_radius=15)
        # Relleno blanco
        pygame.draw.rect(ventana, self.BLANCO, rect_p1, border_radius=15)
        
        txt_p1 = self.fuente_chica.render("1P", True, self.NEGRO)
        ventana.blit(txt_p1, (90, 465))

        # --- Botón P2 ---
        rect_p2 = pygame.Rect(190, 450, 100, 50)
        pygame.draw.rect(ventana, self.NEGRO, (188, 448, 104, 54), border_radius=15)
        pygame.draw.rect(ventana, self.BLANCO, rect_p2, border_radius=15)
        
        txt_p2 = self.fuente_chica.render("2P", True, self.NEGRO)
        ventana.blit(txt_p2, (230, 465))
        
        # --- TEXTO INFORMATIVO ---
        info = self.fuente_chica.render("P1: Solo      P2: Versus", True, self.BLANCO)
        # Le ponemos un fondo negro chiquito al texto para que se lea mejor
        pygame.draw.rect(ventana, (0,0,0), (50, 510, 250, 30)) 
        ventana.blit(info, (55, 515))

    def dibujar_seleccion_clase(self, ventana):
        # 1. DIBUJAR EL FONDO
        try:
            # Ruta absoluta usando la carpeta del proyecto
            ruta_fondo = os.path.join(self.ruta_proyecto, "Imagenes", "Fondo_Elmo.png")
            fondo = pygame.image.load(ruta_fondo)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
        except Exception as e:
            # Si falla la imagen, usa fondo negro
            print(f"Error al cargar fondo_seleccion.png: {e}")
            ventana.fill(self.NEGRO)
        
        # 2. TÍTULO
        texto = self.fuente_grande.render("Elige Clase:", True, self.BLANCO)
        ventana.blit(texto, (100, 50))
                
        # --- CARGAR Y MOSTRAR 4 IMÁGENES EN FILA ---
        # MAPEO: Cada clase con su archivo de imagen
        clases_imagenes = {
            "Agua": "P_Agua.png",
            "Tierra": "P_Tierra.png",
            "Fuego": "P_Fuego.png",
            "Aire": "P_Aire.png"
        }
        
        clases = list(clases_imagenes.keys())
        imagenes_cargadas = []
        
        # Cargar las 4 imágenes
        for clase in clases:
            try:
                Imagenes = clases_imagenes[clase]
                ruta_imagen = os.path.join(self.ruta_proyecto, "Imagenes", Imagenes)
                imagen = pygame.image.load(ruta_imagen)
                imagen = pygame.transform.scale(imagen, (180, 200))  # Redimensionar
                imagenes_cargadas.append(imagen)
            except Exception as e:
                print(f"Error al cargar {clases_imagenes[clase]}: {e}")
                imagenes_cargadas.append(None)
        
        # Mostrar las imágenes en fila
        espacio_x = 220  # Espacio entre imágenes
        y_inicio = 180   # Posición Y
        x_inicio = 50    # Posición X inicial
        
        for i, imagen in enumerate(imagenes_cargadas):
            x_pos = x_inicio + (i * espacio_x)
            
            # Si la imagen se cargó, mostrarla
            if imagen:
                ventana.blit(imagen, (x_pos, y_inicio))
                # Marco alrededor de la imagen
                pygame.draw.rect(ventana, self.BLANCO, (x_pos , y_inicio , 181, 201), 5)
            else:
                # Si falla, mostrar un rectángulo gris
                pygame.draw.rect(ventana, (100, 100, 100), (x_pos, y_inicio, 200, 200))
            
            # Etiqueta debajo de cada imagen
            etiqueta = self.fuente_etiqueta.render(clases[i], True, self.BLANCO)
            # Recuadro detrás de la etiqueta
            rect_etiqueta = etiqueta.get_rect(topleft=(x_pos + 30, y_inicio + 250))
            pygame.draw.rect(ventana, self.NEGRO, rect_etiqueta.inflate(20, 10), border_radius=8)
            pygame.draw.rect(ventana, self.BLANCO, rect_etiqueta.inflate(20, 10), 2, border_radius=8)
            ventana.blit(etiqueta, (x_pos + 30, y_inicio + 250))
            
            

    # --- PANTALLA 3: INTERFAZ DE JUEGO ---
    def dibujar_interfaz_juego(self, ventana, jugador, nombre_carta_actual):
        # 1. EL FONDO
        try:
            # Ruta absoluta usando la carpeta del proyecto
            ruta_fondo = os.path.join(self.ruta_proyecto, "Imagenes", "Fondo_Elmo.png")
            fondo = pygame.image.load(ruta_fondo)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
        except Exception as e:
            # Si falla la imagen, usa fondo marrón oscuro
            print(f"Error al cargar fondo_juego.png: {e}")
            COLOR_TABLERO = (160, 140, 90) 
            ventana.fill(COLOR_TABLERO)

        # 2. ZONA DE LA CARTA (A la IZQUIERDA)
        tiempo = pygame.time.get_ticks() / 1000  # Convertir a segundos
        flotacion = math.sin(tiempo) * 5 
        
        # Marco y Carta
        x_carta = 100
        y_carta = int(150 + flotacion)  # Convertir a entero para Pygame
        rect_carta = pygame.Rect(x_carta, y_carta, 230, 320)
        
        pygame.draw.rect(ventana, (20, 20, 20), rect_carta) 
        COLOR_DORADO = (218, 165, 32)
        pygame.draw.rect(ventana, COLOR_DORADO, rect_carta, 8) 

        # CARGAR Y MOSTRAR IMAGEN DE LA CARTA
        try:
            # Carga la imagen basada en el nombre de la carta
            nombre_imagen = nombre_carta_actual.lower().replace(" ", "_") + ".png"
            ruta_imagen_carta = os.path.join(self.ruta_proyecto, "Imagenes", nombre_imagen)
            imagen_carta = pygame.image.load(ruta_imagen_carta)
            # Redimensionar para que quepa en la tarjeta (dejando espacio para el borde y nombre)
            imagen_carta = pygame.transform.scale(imagen_carta, (200, 220))
            ventana.blit(imagen_carta, (x_carta + 10, y_carta + 20))
        except Exception as e:
            # Si no encuentra la imagen, muestra un rectángulo gris
            print(f"Error al cargar imagen de carta: {e}")
            pygame.draw.rect(ventana, (100, 100, 100), (x_carta + 10, y_carta + 20, 200, 220))

        texto_nombre = self.fuente_chica.render(nombre_carta_actual, True, self.NEGRO)
        ventana.blit(texto_nombre, (x_carta, y_carta - 30))

        # 3. ZONA DE ESTADÍSTICAS (A la DERECHA)
        COLOR_NEON = (0, 255, 255) 
        fuente_gigante = pygame.font.SysFont("Impact", 60) 
        
        texto_lp = fuente_gigante.render(f"LP: {jugador.vidas}000", True, COLOR_NEON)
        texto_lp_sombra = fuente_gigante.render(f"LP: {jugador.vidas}000", True, (0,0,0))
        
        ventana.blit(texto_lp_sombra, (455, 205)) 
        ventana.blit(texto_lp, (450, 200))

        xp_actual = getattr(jugador, 'xp', 0)
        texto_xp = self.fuente_chica.render(f"EXP: {xp_actual}/100", True, self.BLANCO)
        
        # Recuadro para EXP
        rect_xp = pygame.Rect(440, 270, 200, 40)
        pygame.draw.rect(ventana, (0, 0, 0), rect_xp)
        ventana.blit(texto_xp, (450, 280))

        # 4. CAJA DE ATAQUE/DEFENSA
        rect_stats = pygame.Rect(x_carta + 20, y_carta + 250, 190, 50)
        pygame.draw.rect(ventana, (240, 230, 140), rect_stats)
        
        txt_atk = self.fuente_chica.render("ATK/900  DEF/400", True, self.NEGRO)
        ventana.blit(txt_atk, (x_carta + 30, y_carta + 260))