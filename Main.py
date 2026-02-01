import pygame
from Models.Modelos import GameModel
from Views.Interfaz_conf import Interfaz_conf
from Views.Menu_Vista import Menu_Vista
from Views.Juego_Vista import GameView
from Views.Estructura_Vista import Estructura_Vista
<<<<<<< Updated upstream
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
=======
from Views.Combate_Vista import Combate_Vista

# Importamos tus nuevos controladores
from Controllers.MenuControlador import MenuControlador
from Controllers.MapControlador import Mapcontrolador
from Controllers.EvolucionControlador import EvolucionControlador
from Controllers.CombateControlador import CombateControlador
>>>>>>> Stashed changes

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
        
<<<<<<< Updated upstream
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
=======
        # 2. Instanciar Vistas
        self.v_menu = Menu_Vista(self.config)
        self.v_juego = GameView(self.config)
        self.v_estructuras = Estructura_Vista(self.config)
        self.v_combate = Combate_Vista(self.config)

        # 3. Instanciar Controladores (Pasándoles lo que necesitan)
        self.c_menu = MenuControlador(self.model)
        self.c_mapa = Mapcontrolador(self.model, self.v_estructuras)
        self.c_evo = EvolucionControlador(self.model)
        self.c_combate = None  # Se inicializa cuando comienza el combate

        self.estado = "MENU" # Estados: MENU, SELECCION, JUEGO, EVOLUCION, COMBATE, DERROTA
        self.ejecutando = True

    def ejecutar(self):
        while self.ejecutando:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.ejecutando = False

            # --- LÓGICA DE CONTROLADORES (Por Clics) ---
            if self.estado == "MENU":
                self.estado = self.c_menu.inicio(eventos)
            
            elif self.estado == "SELECCION":
                self.estado = self.c_menu.seleccion(eventos)
            
            elif self.estado == "JUEGO":
                # El MapController retorna el resultado del encuentro (Premio, Muerte, etc.)
                resultado = self.c_mapa.gestionar_movimiento(eventos)
                if resultado:
                    if resultado.get("Tipo") == "Muerte":
                        # Iniciar combate
                        self.c_combate = CombateControlador(self.model, self.v_combate)
                        self.estado = "COMBATE"
                    elif resultado.get("SubioNivel"):
                        self.estado = "EVOLUCION"
            
            elif self.estado == "COMBATE":
                self.estado = self.c_combate.ejecutar(eventos)
                if self.estado == "JUEGO":
                    # Cambiar turno después de combate ganado
                    self.model.cambiar_turno()
                elif self.estado == "DERROTA":
                    pass  # Se mostrará la pantalla de derrota
            
            elif self.estado == "EVOLUCION":
                self.estado = self.c_evo.ejecutar(eventos, self.v_estructuras)
            
            elif self.estado == "DERROTA":
                # Esperar a que el jugador presione reintentar
                for evento in eventos:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if self.v_combate.rect_boton_reinicio.collidepoint(evento.pos):
                            # Reiniciar el juego
                            self.estado = "MENU"
                            self.model = GameModel()
                            self.c_menu = MenuControlador(self.model)
                            self.c_mapa = Mapcontrolador(self.model, self.v_estructuras)
                            self.c_evo = EvolucionControlador(self.model)

            # --- RENDERIZADO (Vistas) ---
            if self.estado == "MENU":
                self.v_menu.dibujar_menu(self.ventana)
            
            elif self.estado == "SELECCION":
                self.v_menu.dibujar_seleccion_clase(self.ventana)
            
            elif self.estado == "JUEGO":
                jugador = self.model.obtener_jugador_actual()
                nombre_carta = self.model.info_visual()
                self.v_juego.dibujar_interfaz(self.ventana, jugador, nombre_carta)
                self.v_estructuras.dibujar_mapa_grafo(self.ventana, self.model)
            
            elif self.estado == "EVOLUCION":
                # Pasamos la lógica del árbol a la vista para elegir habilidad
                # Opcionalmente se puede pasar una ruta_fondo: "nombre_archivo.png"
                self.v_estructuras.dibujar_arbol_habilidades(self.ventana, self.model)
            
            elif self.estado == "COMBATE":
                jugador = self.model.obtener_jugador_actual()
                enemigo = self.c_combate.obtener_enemigo()
                log = self.c_combate.obtener_log()
                self.v_combate.dibujar_combate(self.ventana, jugador, enemigo, log)
            
            elif self.estado == "DERROTA":
                jugador = self.model.obtener_jugador_actual()
                self.v_combate.dibujar_derrota(self.ventana, f"El {self.c_combate.enemigo.nombre} fue más fuerte...")
>>>>>>> Stashed changes

    pygame.quit()

if __name__ == "__main__":
    probar_sistema()