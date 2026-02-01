import pygame
import math
import os

class GameView:
    def __init__(self, config):
        self.c = config
        # Localizamos la ruta raíz del proyecto para acceder a la carpeta Imagenes
        self.ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def dibujar_interfaz(self, ventana, jugador, nombre_carta_actual, nodo_actual):
        # 1. DICCIONARIO DE FONDOS DINÁMICOS (Original)
        fondos_nodos = {
            "Inicio": "Fondo_Inicial.png",
            "Comedor": "Fondo_Comedor.png",
            "Campus": "Fondo_Universidad.png",
            "Ed39": "Fondo_Ed39.png",
            "Piso 5": "Fondo_Piso5.png"  
        }

        # --- LÓGICA DE ELMO PARA SUBIDA DE NIVEL ---
        xp_actual = getattr(jugador, 'xp', 0)
        
        # Si la XP es 100, forzamos el fondo de Elmo, si no, usamos el del nodo
        if xp_actual >= 100:
            nombre_archivo = "Elmo_Fondo.png"
        else:
            nombre_archivo = fondos_nodos.get(nodo_actual, "Fondo_Inicial.png")
        
        # 2. DIBUJAR EL FONDO
        try:
            ruta_fondo = os.path.join(self.ruta_proyecto, "Imagenes", nombre_archivo)
            fondo = pygame.image.load(ruta_fondo)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
        except Exception as e:
            # Color de respaldo si no encuentra la imagen
            ventana.fill((160, 140, 90)) 

        # 3. LÓGICA DE LA CARTA FLOTANTE
        tiempo = pygame.time.get_ticks() / 1000  
        flotacion = math.sin(tiempo) * 8  
        
        x_carta = 100
        y_carta = int(150 + flotacion)
        
        try:
            img_nombre = f"P_{jugador.clase}.png"
            ruta_personaje = os.path.join(self.ruta_proyecto, "Imagenes", img_nombre)
            personaje = pygame.image.load(ruta_personaje)
            personaje = pygame.transform.scale(personaje, (230, 320))
            
            # Sombra de la carta
            pygame.draw.rect(ventana, (20, 20, 20), (x_carta + 5, y_carta + 5, 230, 320), border_radius=10)
            ventana.blit(personaje, (x_carta, y_carta))
            # Borde Neón
            pygame.draw.rect(ventana, self.c.NEON, (x_carta, y_carta, 230, 320), 3, border_radius=10)
        except:
            pygame.draw.rect(ventana, (100, 100, 100), (x_carta, y_carta, 230, 320))

        # 4. TEXTOS DE ESTADO (Ajustados para no encimarse)
        txt_nombre = self.c.f_chica.render(nombre_carta_actual, True, self.c.BLANCO)
        ventana.blit(txt_nombre, (x_carta, y_carta - 30))

        # Vida (LP)
        fuente_lp = pygame.font.SysFont("Impact", 60)
        lp_texto = f"LP: {jugador.vidas}000"
        render_lp = fuente_lp.render(lp_texto, True, self.c.NEON)
        ventana.blit(render_lp, (450, 180))

        # Información del Lugar Actual
        txt_lugar = self.c.f_chica.render(f"UBICACIÓN: {nodo_actual}", True, self.c.BLANCO)
        ventana.blit(txt_lugar, (450, 250))

        # --- 5. BARRA DE EXPERIENCIA (ACOPLADA) ---
        xp_maxima = 100
        ancho_barra_px = 250
        
        # El min(..., 1.0) asegura que no se rompa la barra visualmente
        proporcion = min(xp_actual / xp_maxima, 1.0)
        
        txt_xp = self.c.f_chica.render(f"EXP: {xp_actual} / {xp_maxima}", True, self.c.BLANCO)
        ventana.blit(txt_xp, (450, 290))
        
        # Dibujar barra de progreso (Fondo Gris)
        pygame.draw.rect(ventana, (50, 50, 50), (450, 320, ancho_barra_px, 15), border_radius=5)
        
        # Relleno Neón
        if xp_actual > 0:
            pygame.draw.rect(ventana, self.c.NEON, (450, 320, int(ancho_barra_px * proporcion), 15), border_radius=5)
            
        # Borde de la barra para que se vea "cerrada"
        pygame.draw.rect(ventana, self.c.BLANCO, (450, 320, ancho_barra_px, 15), 1, border_radius=5)