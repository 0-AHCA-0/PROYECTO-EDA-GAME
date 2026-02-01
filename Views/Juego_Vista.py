import pygame
import math
import os
# Ajuste basado en tu captura de pantalla:
from Models.ArbolEvolucion import ArbolEvolucion 

class GameView:
    def __init__(self, config):
        self.c = config
        self.ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Instanciamos tu clase para obtener los textos
        self.arbol_logica = ArbolEvolucion()

    def buscar_imagen_inteligente(self, nombre_diccionario, clase_jugador):
        """
        Busca el archivo correcto ignorando prefijos (F_, EF_, etc), 
        mayúsculas y palabras conectoras como 'en' o 'del'.
        """
        carpeta_imgs = os.path.join(self.ruta_proyecto, "Imagenes")
        
        # 1. Normalizar el nombre del diccionario (minusculas y sin espacios)
        nombre_clave = nombre_diccionario.replace(" ", "_").lower()
        
        # 2. Crear versiones alternativas para encontrar el archivo
        # Quitamos "en_" y "del_" por si el archivo no los tiene (caso Fuego)
        nombre_clave_corto = nombre_clave.replace("_en_", "_").replace("_del_", "_")
        
        archivos_encontrados = []
        
        try:
            todos_archivos = os.listdir(carpeta_imgs)
        except:
            return f"P_{clase_jugador}.png" # Fallback si falla la carpeta

        for archivo in todos_archivos:
            archivo_lower = archivo.lower()
            
            # Solo miramos PNGs o JPGs
            if not (archivo_lower.endswith(".png") or archivo_lower.endswith(".jpg")):
                continue

            # CRITERIO 1: Coincidencia exacta (Ej: "T_Semilla.png" contiene "semilla")
            if nombre_clave in archivo_lower:
                return archivo
            
            # CRITERIO 2: Coincidencia sin conectores (Ej: Encuentra "experto_fuego" en "EF_Experto_Fuego.png")
            if nombre_clave_corto in archivo_lower:
                return archivo

        # Si no encuentra nada, devuelve una por defecto para que no crashee
        return f"P_{clase_jugador}.png"

    def dibujar_interfaz(self, ventana, jugador, nombre_carta_actual, nodo_actual):
        # 1. OBTENER EL NOMBRE DEL DICCIONARIO
        # Esto trae "Aprendiz Hot", "Experto en Fuego", etc.
        nombre_evolucion = self.arbol_logica.obtener_nombre_evolucion(jugador.clase, jugador.nivel_evolucion)
        
        if nombre_evolucion == "Desconocido":
            nombre_evolucion = nombre_carta_actual

        # 2. FONDO (Lógica de Elmo)
        fondos_nodos = {
            "Inicio": "Fondo_Inicial.png", "Comedor": "Fondo_Comedor.png",
            "Campus": "Fondo_Universidad.png", "Ed39": "Fondo_Ed39.png", "Piso 5": "Fondo_Piso5.png"  
        }

        xp_actual = getattr(jugador, 'xp', 0)
        
        # Usamos tu imagen "Fondo_Habilidad.jpg" o "Elmo" cuando está al máximo
        if xp_actual >= 100:
            nombre_archivo_fondo = "Fondo_Habilidad.jpg" # O Elmo_Fondo.png si prefieres
        else:
            nombre_archivo_fondo = fondos_nodos.get(nodo_actual, "Fondo_Inicial.png")
        
        try:
            ruta_fondo = os.path.join(self.ruta_proyecto, "Imagenes", nombre_archivo_fondo)
            if os.path.exists(ruta_fondo):
                fondo = pygame.image.load(ruta_fondo)
                fondo = pygame.transform.scale(fondo, (930, 600))
                ventana.blit(fondo, (0, 0))
            else:
                ventana.fill((20, 20, 30))
        except:
            ventana.fill((20, 20, 30)) 

        # 3. CARTA FLOTANTE
        tiempo = pygame.time.get_ticks() / 1000  
        flotacion = math.sin(tiempo) * 8  
        x_carta, y_carta = 100, int(150 + flotacion)
        
        try:
            # --- AQUÍ USAMOS LA BÚSQUEDA INTELIGENTE ---
            # Le pasamos "Experto en Fuego" y ella encuentra "EF_Experto_Fuego.png" sola.
            nombre_archivo_img = self.buscar_imagen_inteligente(nombre_evolucion, jugador.clase)
            
            ruta_personaje = os.path.join(self.ruta_proyecto, "Imagenes", nombre_archivo_img)
            
            # Cargar imagen
            if os.path.exists(ruta_personaje):
                personaje = pygame.image.load(ruta_personaje)
            else:
                # Si falló la inteligente, intenta cargar una genérica
                personaje = pygame.image.load(os.path.join(self.ruta_proyecto, "Imagenes", "fondo.png"))

            personaje = pygame.transform.scale(personaje, (230, 320))
            
            # Sombra y Carta
            pygame.draw.rect(ventana, (20, 20, 20), (x_carta + 5, y_carta + 5, 230, 320), border_radius=10)
            ventana.blit(personaje, (x_carta, y_carta))
            
            # Borde según nivel
            colores = {1: self.c.NEON, 2: (255, 215, 0), 3: (255, 50, 50)}
            color_borde = colores.get(int(jugador.nivel_evolucion), self.c.NEON)
                
            pygame.draw.rect(ventana, color_borde, (x_carta, y_carta, 230, 320), 3, border_radius=10)
        except Exception as e:
            print(f"Error dibujando carta: {e}")
            pygame.draw.rect(ventana, (100, 100, 100), (x_carta, y_carta, 230, 320))

        # 4. TEXTO NOMBRE (Centrado sobre la carta)
        txt_nombre = self.c.f_chica.render(nombre_evolucion, True, self.c.BLANCO)
        ancho_txt = txt_nombre.get_width()
        ventana.blit(txt_nombre, (x_carta + (230 - ancho_txt)//2, y_carta - 30))

        # 5. UI RESTANTE
        fuente_lp = pygame.font.SysFont("Impact", 60)
        ventana.blit(fuente_lp.render(f"LP: {jugador.vidas}000", True, self.c.NEON), (450, 180))
        ventana.blit(self.c.f_chica.render(f"UBICACIÓN: {nodo_actual}", True, self.c.BLANCO), (450, 250))
        
        # Barra XP
        xp_maxima = 100
        ancho_barra = 250
        prop = min(xp_actual / xp_maxima, 1.0)
        ventana.blit(self.c.f_chica.render(f"EXP: {xp_actual} / {xp_maxima}", True, self.c.BLANCO), (450, 290))
        
        pygame.draw.rect(ventana, (50, 50, 50), (450, 320, ancho_barra, 15), border_radius=5)
        if xp_actual > 0:
            pygame.draw.rect(ventana, self.c.NEON, (450, 320, int(ancho_barra * prop), 15), border_radius=5)
        pygame.draw.rect(ventana, self.c.BLANCO, (450, 320, ancho_barra, 15), 1, border_radius=5)