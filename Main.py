import pygame
from Models.Modelos import GameModel
from Views.Interfaz_conf import Interfaz_conf
from Views.Menu_Vista import Menu_Vista
from Views.Juego_Vista import GameView
from Views.Estructura_Vista import Estructura_Vista
#Por el momento es solo un main de prueba
def probar_sistema():
    pygame.init()
    ventana = pygame.display.set_mode((930, 600))
    pygame.display.set_caption("TEST")
    reloj = pygame.time.Clock()

    # 1. Instanciar el motor
    config = Interfaz_conf()
    model = GameModel()
    
    # 2. Instanciar vistas
    v_menu = Menu_Vista(config)
    v_juego = GameView(config)
    v_estructuras = Estructura_Vista(config)

    # 3. Datos de prueba: Creamos un jugador inicial
    model.agregar_jugador(1, "Fuego")
    
    estado = "MENU"
    ejecutando = True

    print("--- CONTROLES DE PRUEBA ---")
    print("1: Menú | 2: Selección | 3: Juego | 4: Evolución (Test)")
    print("G: Guardar CSV | M: Mover a Campus (Grafo)")

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            # Simulación de Controlador (Lo que haría Erick)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1: estado = "MENU"
                if evento.key == pygame.K_2: estado = "SELECCION"
                if evento.key == pygame.K_3: estado = "JUEGO"
                if evento.key == pygame.K_g: 
                    model.guardar_todo()
                    print("Archivo CSV actualizado")
                if evento.key == pygame.K_m:
                    # Probamos tu lógica de movimiento y grafos
                    resultado = model.procesar_movimiento("Campus")
                    print(f"Resultado del nodo: {resultado}")

        # --- RENDERIZADO SEGÚN ESTADO ---
        if estado == "MENU":
            v_menu.dibujar_menu(ventana)
        
        elif estado == "SELECCION":
            v_menu.dibujar_seleccion_clase(ventana)
        
        elif estado == "JUEGO":
            jugador = model.obtener_jugador_actual()
            nombre_carta = model.info_visual()
            
            # Dibujamos la parte de Deysi
            v_juego.dibujar_interfaz(ventana, jugador, nombre_carta)
            # Dibujamos TU parte (El Grafo)
            v_estructuras.dibujar_mapa_grafo(ventana, model)

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

if __name__ == "__main__":
    probar_sistema()