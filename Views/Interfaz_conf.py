import pygame
import os
#Holap, esta clase sirve para los colores del fondo
class Interfaz_conf:
    def __init__(self):
        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
        self.AZUL = (50, 50, 200)
        self.NEON = (0, 255, 255)
        
        self.ruta_base = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        #Verificamos fuentes y archivos
        try:
            ruta_f1 = os.path.join(self.ruta_base, "Fuentes", "Tipo1.ttf")
            ruta_f2 = os.path.join(self.ruta_base, "Fuentes", "Tipo2.ttf")
            self.f_grande = pygame.font.Font(ruta_f1, 50)
            self.f_chica = pygame.font.Font(ruta_f2, 20)
        except:
            self.f_grande = pygame.font.SysFont("Arial", 50)
            self.f_chica = pygame.font.SysFont("Arial", 20)
        
    