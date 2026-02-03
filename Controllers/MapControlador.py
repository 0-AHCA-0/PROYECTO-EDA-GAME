import pygame
import math

class Mapcontrolador:
    def __init__(self, modelo, vista_estructuras):
        self.model = modelo
        self.v_struct = vista_estructuras
    
    def gestionar_movimiento(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Revisamos si el clic dio en algún nodo del mapa
                for nombre_nodo, coords in self.v_struct.posiciones_mapa.items():
                    dist = math.hypot(evento.pos[0] - coords[0], evento.pos[1] - coords[1])
                    if dist <= 30: # Radio de colisión
                        # El modelo valida si el movimiento es legal y devuelve el evento
                        resultado = self.model.procesar_movimiento(nombre_nodo)
                        return resultado
        return None