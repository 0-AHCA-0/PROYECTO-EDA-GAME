import pygame
import math

class Mapcontrolador:
    def __init__(self, modelo, vista_estructuras):
        # Referencia al modelo para la logica de datos
        self.model = modelo
        # Referencia a la vista para conocer las coordenadas de los nodos
        self.v_struct = vista_estructuras
    
    def gestionar_movimiento(self, eventos):
        """
        Detecta la interaccion del usuario con los nodos del mapa.
        Calcula colisiones circulares para determinar a que lugar se hizo clic.
        """
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Recorremos todas las posiciones definidas en la vista
                for nombre_nodo, coords in self.v_struct.posiciones_mapa.items():
                    # Formula de distancia euclidiana para detectar el clic en el circulo
                    dist = math.hypot(evento.pos[0] - coords[0], evento.pos[1] - coords[1])
                    
                    # Si la distancia es menor al radio, el usuario toco el nodo
                    if dist <= 30: 
                        # IMPORTANTE: El modelo es quien decide si el salto es valido
                        # y nos devuelve que evento ocurre (Combate, Muerte, Premio, etc.)
                        resultado = self.model.procesar_movimiento(nombre_nodo)
                        
                        # Retornamos la decision del Sistema de Encuentros al Maestro
                        return resultado
                        
        # Si no hubo clic en ningun nodo valido, no pasa nada
        return None