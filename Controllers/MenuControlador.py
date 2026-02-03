import pygame

class MenuControlador:
    def __init__(self, modelo):
        self.model = modelo
    
    def inicio(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Botones 1P y 2P según tus coordenadas
                if pygame.Rect(50, 450, 100, 50).collidepoint(evento.pos):
                    self.model.modo_juego = 1 
                    self.model.jugadores = [] 
                    return "SELECCION"
                
                if pygame.Rect(190, 450, 100, 50).collidepoint(evento.pos):
                    self.model.modo_juego = 2 
                    self.model.jugadores = []
                    return "SELECCION"
        return "MENU"
    
    def seleccion(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i in range(4):
                    # Coordenadas exactas de tus 4 cartas
                    x_pos = 50 + (i * 220)
                    rect_carta = pygame.Rect(x_pos, 180, 180, 200)
                    
                    if rect_carta.collidepoint(evento.pos):
                        clases = ["Fuego", "Agua", "Tierra", "Aire"]
                        clase_elegida = clases[i]
                        
                        # ID basado en cuántos van (1 o 2)
                        id_nuevo = len(self.model.jugadores) + 1
                        
                        # LLAMADA CRÍTICA:
                        # Asegúrate de que self.model sea la instancia de GameModel
                        self.model.agregar_jugador(id_nuevo, clase_elegida)
                        
                        # Control de flujo para 1P o 2P
                        if self.model.modo_juego == 2 and len(self.model.jugadores) < 2:
                            return "SELECCION" # Falta el segundo jugador
                        else:
                            return "JUEGO" # Todos listos
                            
        return "SELECCION"