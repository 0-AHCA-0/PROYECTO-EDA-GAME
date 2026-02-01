import pygame

class MenuControlador:
    def __init__(self, modelo):
        self.model = modelo
    
    def inicio(self, eventos):
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    # BOTÓN 1P: rect(50, 450, 100, 50)
                    if pygame.Rect(50, 450, 100, 50).collidepoint(evento.pos):
                        self.model.modo_juego = 1 # Guardamos en el modelo que es solo 1
                        return "SELECCION"
                    
                    # BOTÓN 2P: rect(190, 450, 100, 50) <- ESTE ES EL QUE FALTA
                    if pygame.Rect(190, 450, 100, 50).collidepoint(evento.pos):
                        self.model.modo_juego = 2 # Le avisamos al modelo que vienen dos
                        print("Modo 2 Jugadores activado")
                        return "SELECCION"
            return "MENU"
    
    def seleccion(self, eventos):
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(4):
                        x_pos = 50 + (i * 220)
                        if pygame.Rect(x_pos, 180, 180, 200).collidepoint(evento.pos):
                            clases = ["Agua", "Tierra", "Fuego", "Aire"]
                            
                            # Agregamos al jugador actual
                            self.model.agregar_jugador(len(self.model.jugadores) + 1, clases[i])
                            
                            # Si elegimos 2P y solo va un jugador, REINICIAMOS la pantalla
                            if self.model.modo_juego == 2 and len(self.model.jugadores) < 2:
                                return "SELECCION" 
                            else:
                                return "JUEGO"
            return "SELECCION"
