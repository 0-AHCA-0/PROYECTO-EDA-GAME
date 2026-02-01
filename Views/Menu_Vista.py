import pygame
import os
# Importamos el modelo para saber los nombres oficiales (Aprendiz Hot, etc.)
from Models.ArbolEvolucion import ArbolEvolucion 

class Menu_Vista:
    def __init__(self, config):
        """Recibe la configuración de colores y fuentes"""
        self.c = config
        self.ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Instanciamos la lógica para consultar los nombres de Nivel 1
        self.arbol_logica = ArbolEvolucion()

    def buscar_imagen_inteligente(self, nombre_diccionario, clase_jugador):
        """
        Búsqueda avanzada: Separa el nombre en palabras clave e ignora 

        """
        carpeta_imgs = os.path.join(self.ruta_proyecto, "Imagenes")
        
        # 1. Lista de palabras "basura" que ignoraremos para la búsqueda
        conectores = ["el", "la", "los", "las", "un", "una", "de", "del", "en", "y", "o"]

        # 2. Limpiamos el nombre del diccionario
        # Convertimos a minúsculas y quitamos guiones bajos por espacios para separar bien
        nombre_limpio = nombre_diccionario.lower().replace("_", " ")
        palabras = nombre_limpio.split()

        # 3. Filtramos: Nos quedamos solo con palabras útiles (largo > 2 y que no sean conectores)
        palabras_clave = [p for p in palabras if p not in conectores and len(p) > 2]
        # Ej: ['duro', 'como', 'piedra']

        try:
            todos_archivos = os.listdir(carpeta_imgs)
        except:
            return f"P_{clase_jugador}.png"

        # 4. Búsqueda en los archivos
        for archivo in todos_archivos:
            archivo_lower = archivo.lower()
            
            if not (archivo_lower.endswith(".png") or archivo_lower.endswith(".jpg")):
                continue

            # VERIFICACIÓN: ¿Todas las palabras clave están en este archivo?
            coinciden_todas = True
            for palabra in palabras_clave:
                if palabra not in archivo_lower:
                    coinciden_todas = False
                    break
            
            # Si coinciden todas las palabras clave, ¡ESTA ES LA IMAGEN!
            if coinciden_todas:
                return archivo

        # Si no encuentra nada, devuelve la imagen base de la clase (Ej: P_Tierra.png)
        # IMPORTANTE: Ya no devuelve imágenes random, sino la base de tu clase.
        return f"P_{clase_jugador}.png"

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
            # Si no existe Fondo_Elmo, intenta con fondo.png
            if not os.path.exists(ruta_fondo):
                ruta_fondo = os.path.join(self.ruta_proyecto, "Imagenes", "fondo.png")
                
            fondo = pygame.image.load(ruta_fondo)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
        except Exception as e:
            ventana.fill(self.c.NEGRO)
        
        # 2. TÍTULO
        texto = self.c.f_grande.render("Elige tu Elemento:", True, self.c.BLANCO)
        ventana.blit(texto, (100, 50))
                
        # 3. CARGAR CLASES DINÁMICAMENTE
        # Lista de clases disponibles
        lista_clases = ["Fuego", "Agua", "Tierra", "Aire"]
        
        espacio_x = 220 
        y_inicio = 180   
        x_inicio = 50    
        
        for i, clase in enumerate(lista_clases):
            x_pos = x_inicio + (i * espacio_x)
            
            # A) OBTENER NOMBRE REAL DE NIVEL 1 (Ej: "Aprendiz Hot")
            nombre_lv1 = self.arbol_logica.obtener_nombre_evolucion(clase, 1)
            if nombre_lv1 == "Desconocido": 
                nombre_lv1 = clase # Fallback

            # B) BUSCAR LA IMAGEN AUTOMÁTICAMENTE
            # Esto encontrará "F_Aprendiz_Hot.png" o "A_Gota_Joven.png"
            nombre_archivo = self.buscar_imagen_inteligente(nombre_lv1, clase)

            try:
                ruta_img = os.path.join(self.ruta_proyecto, "Imagenes", nombre_archivo)
                if os.path.exists(ruta_img):
                    imagen = pygame.image.load(ruta_img)
                else:
                    # Si falla, carga un placeholder (cuadro gris)
                    raise Exception("Imagen no encontrada")
                    
                imagen = pygame.transform.scale(imagen, (180, 200))
                ventana.blit(imagen, (x_pos, y_inicio))
                
                # Borde blanco
                pygame.draw.rect(ventana, self.c.BLANCO, (x_pos, y_inicio, 181, 201), 5)
                
            except:
                pygame.draw.rect(ventana, (60, 60, 60), (x_pos, y_inicio, 180, 200))
                pygame.draw.rect(ventana, self.c.BLANCO, (x_pos, y_inicio, 180, 200), 2)
            
            # C) ETIQUETA CON EL NOMBRE "COOL" (Ej: Aprendiz Hot)
            # Renderizamos el nombre específico en lugar de solo "Fuego"
            etiqueta = self.c.f_chica.render(nombre_lv1, True, self.c.BLANCO) 
            
            # Fondo negro para la etiqueta
            rect_etiqueta = etiqueta.get_rect(center=(x_pos + 90, y_inicio + 230))
            bg_etiqueta = rect_etiqueta.inflate(20, 10)
            pygame.draw.rect(ventana, self.c.NEGRO, bg_etiqueta, border_radius=8)
            pygame.draw.rect(ventana, self.c.NEON, bg_etiqueta, 2, border_radius=8) # Borde neón
            
            ventana.blit(etiqueta, rect_etiqueta)