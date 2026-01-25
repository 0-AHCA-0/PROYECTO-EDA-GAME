import pygame
import sys
# Importamos tu clase desde la carpeta donde la guardaste
# Si tu carpeta se llama 'Interfaz_Usuario', déjalo así. Si se llama 'Vistas', cámbialo.
from Interfaz_usuario import VistaJuego 

# --- SIMULADOR DE DATOS ---
# Creamos un jugador falso porque aún no tenemos el de Aidan conectado
class JugadorFalso:
    def __init__(self):
        self.vidas = 5      # Probamos con 5 vidas
        self.xp = 150       # Probamos con 150 de experiencia
        self.nivel_evolucion = 1

# --- CONFIGURACIÓN DE PANTALLA ---
pygame.init()
PANTALLA_ANCHO = 930
PANTALLA_ALTO = 600
ventana = pygame.display.set_mode((PANTALLA_ANCHO, PANTALLA_ALTO))
pygame.display.set_caption("Prueba de Deysi - Vista")

# --- INICIO ---
# Aquí nace tu clase Vista
mi_vista = VistaJuego()
mi_jugador = JugadorFalso()

# Variables de prueba
nombre_carta = "P_Fuego" 
modo_prueba = 1 # 1=Menu, 2=Seleccion, 3=Juego (Cambia esto para ver otras pantallas)

# --- BUCLE PRINCIPAL (Esto mantiene la ventana abierta) ---
reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
    # 1. Escuchar si cierran la ventana
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        
        # Truco: Presiona teclas para cambiar de pantalla y probar todo rápido
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1: modo_prueba = 1
            if evento.key == pygame.K_2: modo_prueba = 2
            if evento.key == pygame.K_3: modo_prueba = 3

    # 2. Dibujar lo que toque
    if modo_prueba == 1:
        mi_vista.dibujar_menu(ventana)
    elif modo_prueba == 2:
        mi_vista.dibujar_seleccion_clase(ventana)
    elif modo_prueba == 3:
        # Aquí pasamos los datos falsos para ver cómo quedan
        mi_vista.dibujar_interfaz_juego(ventana, mi_jugador, nombre_carta)

    # 3. Actualizar pantalla
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()