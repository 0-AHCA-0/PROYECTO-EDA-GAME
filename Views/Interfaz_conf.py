import pygame
import os

# Esta clase guarda los colores y las fuentes para que todo el juego se vea igual
class Interfaz_conf:
    def __init__(self):
        # COLORES
        # Definicion de la paleta en formato RGB
        self.NEGRO = (0, 0, 0)
        self.BLANCO = (255, 255, 255)
        self.NEON = (0, 255, 255) # Cyan brillante para resaltar interfaces
        self.AZUL = (0, 100, 255) # Azul para las conexiones del mapa
        
        # RUTA DE ARCHIVOS
        # Busca la carpeta Fuentes subiendo un nivel desde donde esta este script
        dir_views = os.path.dirname(os.path.abspath(__file__))
        self.ruta_fuentes = os.path.normpath(os.path.join(dir_views, "..", "Fuentes"))

        # CONFIGURACION DE TEXTOS
        # Fuente Grande: Para anuncios como LEVEL UP o DERROTA
        self.f_grande = self._cargar_f("Tipo1.ttf", 45) 
        
        # Fuente Media: Para nombres de ataques y textos de botones
        self.f_media = self._cargar_f("Tipo2.ttf", 24) 
        
        # Fuente Chica: Para estadisticas, vida y el historial de daño
        self.f_chica = self._cargar_f("Tipo3.ttf", 16)

    def _cargar_f(self, nombre_archivo, tamano):
        """
        Funcion interna para cargar las letras de forma segura.
        Si no encuentra el archivo, usa una de sistema para que el juego no se cierre.
        """
        ruta_final = os.path.join(self.ruta_fuentes, nombre_archivo)
        
        # Ayuda a que el juego funcione en Linux si hay diferencias de mayusculas
        if not os.path.exists(ruta_final):
            try:
                archivos = os.listdir(self.ruta_fuentes)
                for f in archivos:
                    if f.lower() == nombre_archivo.lower():
                        ruta_final = os.path.join(self.ruta_fuentes, f)
                        break
            except: pass

        # Intenta cargar la fuente personalizada
        if os.path.exists(ruta_final):
            try:
                return pygame.font.Font(ruta_final, tamano)
            except Exception as e:
                print(f"Error en fuente: {e}")
        
        # Si no hay fuente personalizada, usa una generica de respaldo
        return pygame.font.SysFont("DejaVu Sans", tamano)