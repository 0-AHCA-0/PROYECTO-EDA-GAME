import pygame

class Estructura_Vista:
    def __init__(self, config):
        self.c = config
        # Coordenadas estratégicas para que el Grafo no tape la carta de Deysi
        # Se dibuja en la mitad derecha de la pantalla (X entre 600 y 900)
        self.posiciones_mapa = {
            "Inicio": (750, 500),
            "Campus": (650, 380),
            "Comedor": (850, 380),
            "Ed39": (750, 250),
            "Piso 5": (750, 100)
        }

    def dibujar_mapa_grafo(self, ventana, modelo):
        """Renderiza el Grafo Dirigido de rutas del juego"""
        # 1. Dibujar las Aristas (Líneas de conexión)
        for origen, destinos in modelo.encuentros.grafo_mapa.items():
            for destino in destinos:
                if origen in self.posiciones_mapa and destino in self.posiciones_mapa:
                    pygame.draw.line(
                        ventana, 
                        self.c.AZUL, 
                        self.posiciones_mapa[origen], 
                        self.posiciones_mapa[destino], 
                        4
                    )

        # 2. Dibujar los Nodos (Círculos interactivos)
        jugador = modelo.obtener_jugador_actual()
        for nodo, pos in self.posiciones_mapa.items():
            # El nodo actual brilla en Neón, los demás en gris oscuro
            es_actual = (nodo == jugador.nodo_actual)
            color_nodo = self.c.COLOR_NEON if es_actual else (60, 60, 60)
            
            # Dibujo del nodo con borde
            pygame.draw.circle(ventana, color_nodo, pos, 25)
            pygame.draw.circle(ventana, self.c.BLANCO, pos, 25, 2)
            
            # Nombre del lugar debajo del círculo
            txt_nodo = self.c.f_chica.render(nodo, True, self.c.BLANCO)
            ventana.blit(txt_nodo, (pos[0] - 25, pos[1] + 30))

    def dibujar_arbol_habilidades(self, ventana, modelo):
        """Pantalla especial para la elección binaria de habilidades (Árbol)"""
        # Fondo semi-transparente para resaltar la elección
        superficie_overlay = pygame.Surface((930, 600), pygame.SRCALPHA)
        superficie_overlay.fill((0, 0, 0, 180)) 
        ventana.blit(superficie_overlay, (0,0))

        jugador = modelo.obtener_jugador_actual()
        opciones = modelo.evolucionar_jugador() # Obtiene los hijos del nodo actual

        titulo = self.c.f_grande.render("¡NUEVA HABILIDAD DISPONIBLE!", True, self.c.COLOR_NEON)
        ventana.blit(titulo, (150, 100))

        # Dibujar las dos ramas del árbol (Izquierda y Derecha)
        for i, habilidad in enumerate(opciones):
            x_pos = 200 + (i * 350)
            rect_boton = pygame.Rect(x_pos, 300, 220, 80)
            
            # Diseño del botón de habilidad
            pygame.draw.rect(ventana, self.c.BLANCO, rect_p1, border_radius=15)
            pygame.draw.rect(ventana, self.c.COLOR_NEON, rect_boton, 3, border_radius=15)
            
            txt_hab = self.c.f_chica.render(habilidad, True, self.c.BLANCO)
            ventana.blit(txt_hab, (x_pos + 20, 330))