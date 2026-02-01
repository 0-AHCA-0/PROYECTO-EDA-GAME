import pygame

class MenuControlador:
    def __init__(self, modelo):
        self.model = modelo
    
    def inicio(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # BOTÓN 1P: rect(50, 450, 100, 50)
                if pygame.Rect(50, 450, 100, 50).collidepoint(evento.pos):
                    self.model.modo_juego = 1 
                    # Reiniciamos la lista de jugadores por si acaso vienes de una partida anterior
                    self.model.jugadores = [] 
                    print("Modo seleccionado: 1 Jugador")
                    return "SELECCION"
                
                # BOTÓN 2P: rect(190, 450, 100, 50)
                if pygame.Rect(190, 450, 100, 50).collidepoint(evento.pos):
                    self.model.modo_juego = 2 
                    self.model.jugadores = []
                    print("Modo seleccionado: 2 Jugadores")
                    return "SELECCION"
        return "MENU"
    
    def seleccion(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i in range(4):
                    # Coordenadas de las cartas (mismas que en la vista)
                    x_pos = 50 + (i * 220)
                    rect_carta = pygame.Rect(x_pos, 180, 180, 200)
                    
                    if rect_carta.collidepoint(evento.pos):
                        # --- CORRECCIÓN AQUÍ: EL ORDEN DEBE SER IGUAL A LA VISTA ---
                        clases = ["Fuego", "Agua", "Tierra", "Aire"]
                        clase_elegida = clases[i]
                        
                        # Calculamos ID del jugador (1 o 2)
                        id_nuevo = len(self.model.jugadores) + 1
                        
                        # Agregamos al modelo
                        self.model.agregar_jugador(id_nuevo, clase_elegida)
                        print(f"Jugador {id_nuevo} eligió: {clase_elegida}")
                        
                        # LÓGICA DE TRANSICIÓN
                        modo = getattr(self.model, "modo_juego", 1) # Por defecto 1 si no existe
                        
                        # Si es modo 2P y falta elegir al segundo...
                        if modo == 2 and len(self.model.jugadores) < 2:
                            # Esperamos al siguiente clic (No cambiamos de estado)
                            return "SELECCION" 
                        else:
                            # Ya están todos listos, ¡A JUGAR!
                            print("¡Todos listos! Iniciando juego...")
                            return "JUEGO"
                            
        return "SELECCION"