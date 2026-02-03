import pygame
import os

class Interfaz_conf:
    def __init__(self):
        # --- COLORES ---
        self.NEGRO = (0, 0, 0)
        self.BLANCO = (255, 255, 255)
        self.NEON = (0, 255, 255)
        self.AZUL = (0, 100, 255)
        
        # --- RUTA ABSOLUTA (Basada en tu estructura real) ---
        dir_views = os.path.dirname(os.path.abspath(__file__))
        self.ruta_fuentes = os.path.normpath(os.path.join(dir_views, "..", "Fuentes"))

        # --- CARGA DE FUENTES CON TAMAÑOS REDUCIDOS ---
        # Grande: Bajamos de 55 a 45 para que no choque con los bordes
        self.f_grande = self._cargar_f("Tipo1.ttf", 45) 
        
        # Media: Bajamos de 32 a 24 para que los nombres de ataques quepan en los botones
        self.f_media = self._cargar_f("Tipo2.ttf", 24) 
        
        # Chica: Bajamos de 18 a 16 para que el log de combate no se amontone
        self.f_chica = self._cargar_f("Tipo3.ttf", 16)

    def _cargar_f(self, nombre_archivo, tamano):
        ruta_final = os.path.join(self.ruta_fuentes, nombre_archivo)
        
        # Mapeo de nombres para Linux (case-insensitive)
        if not os.path.exists(ruta_final):
            try:
                archivos = os.listdir(self.ruta_fuentes)
                for f in archivos:
                    if f.lower() == nombre_archivo.lower():
                        ruta_final = os.path.join(self.ruta_fuentes, f)
                        break
            except: pass

        if os.path.exists(ruta_final):
            try:
                return pygame.font.Font(ruta_final, tamano)
            except Exception as e:
                print(f"Error en fuente: {e}")
        
        return pygame.font.SysFont("DejaVu Sans", tamano)