import pygame

class MenuControlador:
    def __init__(self, modelo):
        # El controlador guarda una referencia al modelo para actualizar el estado global
        self.model = modelo
    
    def inicio(self, eventos):
        """
        Gestiona la pantalla principal donde se elige la cantidad de jugadores.
        """
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # BOTON 1 JUGADOR (1P): Setea el modo y limpia la lista de personajes
                if pygame.Rect(50, 450, 100, 50).collidepoint(evento.pos):
                    self.model.modo_juego = 1 
                    self.model.jugadores = [] 
                    return "SELECCION"
                
                # BOTON 2 JUGADORES (2P): Modo cooperativo o por turnos
                if pygame.Rect(190, 450, 100, 50).collidepoint(evento.pos):
                    self.model.modo_juego = 2 
                    self.model.jugadores = []
                    return "SELECCION"
                    
        # Si no hay clics en los botones, el estado se mantiene igual
        return "MENU"
    
    def seleccion(self, eventos):
        """
        Gestiona la pantalla de eleccion de clase (Fuego, Agua, Tierra, Aire).
        Soporta la seleccion secuencial para 2 jugadores si es necesario.
        """
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Revisamos las 4 cartas disponibles en la interfaz
                for i in range(4):
                    # Calculo de la posicion X basado en el indice de la carta
                    x_pos = 50 + (i * 220)
                    rect_carta = pygame.Rect(x_pos, 180, 180, 200)
                    
                    if rect_carta.collidepoint(evento.pos):
                        # Mapeo de la posicion a la clase elemental correspondiente
                        clases = ["Fuego", "Agua", "Tierra", "Aire"]
                        clase_elegida = clases[i]
                        
                        # Generacion de ID (Jugador 1 o Jugador 2)
                        id_nuevo = len(self.model.jugadores) + 1
                        
                        # El modelo crea la instancia de la clase elegida y la guarda
                        self.model.agregar_jugador(id_nuevo, clase_elegida)
                        
                        # LOGICA DE TRANSICION:
                        # Si es modo 2P y solo hay un jugador, vuelve a pedir seleccion
                        if self.model.modo_juego == 2 and len(self.model.jugadores) < 2:
                            return "SELECCION" 
                        else:
                            # Si es 1P o ya estan los dos de 2P, iniciamos la partida
                            return "JUEGO" 
                            
        return "SELECCION"