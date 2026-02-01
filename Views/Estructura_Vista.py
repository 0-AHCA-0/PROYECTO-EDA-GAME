import pygame
import os

class Estructura_Vista:
    def __init__(self, config):
        self.c = config
        self.botones_evolucion = []  # Almacena los Rect de los botones para detección de clics
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
            color_nodo = self.c.NEON if es_actual else (60, 60, 60)
            
            # Dibujo del nodo con borde
            pygame.draw.circle(ventana, color_nodo, pos, 25)
            pygame.draw.circle(ventana, self.c.BLANCO, pos, 25, 2)
            
            # Nombre del lugar debajo del círculo
            txt_nodo = self.c.f_chica.render(nodo, True, self.c.BLANCO)
            ventana.blit(txt_nodo, (pos[0] - 25, pos[1] + 30))

    def dibujar_arbol_habilidades(self, ventana, modelo, ruta_fondo=None):
        """
        Pantalla especial para la elección binaria de habilidades (Árbol).
        
        Args:
            ventana: Superficie de Pygame para dibujar
            modelo: GameModel con información del jugador
            ruta_fondo: Ruta opcional a imagen de fondo en carpeta Imagenes
        """
        # 1. Cargar fondo dinámico si se proporciona, si no usar overlay oscuro
        if ruta_fondo:
            try:
                ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                ruta_img_fondo = os.path.join(ruta_proyecto, "Imagenes", ruta_fondo)
                fondo = pygame.image.load(ruta_img_fondo)
                fondo = pygame.transform.scale(fondo, (930, 600))
                ventana.blit(fondo, (0, 0))
            except Exception as e:
                print(f"Error cargando fondo: {e}")
                # Respaldo a color oscuro si falla la carga
                ventana.fill((20, 20, 30))
        else:
            # Fondo semi-transparente por defecto
            superficie_overlay = pygame.Surface((930, 600), pygame.SRCALPHA)
            superficie_overlay.fill((0, 0, 0, 180)) 
            ventana.blit(superficie_overlay, (0, 0))

        # 2. Limpiar botones previos para almacenar los nuevos
        self.botones_evolucion = []

        jugador = modelo.obtener_jugador_actual()
        opciones = modelo.evolucionar_jugador()  # Obtiene los hijos del nodo actual

        # 3. Título principal
        titulo = self.c.f_grande.render("¡NUEVA HABILIDAD DISPONIBLE!", True, self.c.NEON)
        ventana.blit(titulo, (150, 100))

        # 4. Dibujar las dos ramas del árbol (Izquierda y Derecha)
        for i, habilidad in enumerate(opciones):
            x_pos = 200 + (i * 350)
            rect_boton = pygame.Rect(x_pos, 300, 220, 80)
            
            # Guardar el rect para detección de clics en el controlador
            self.botones_evolucion.append({
                "rect": rect_boton,
                "habilidad": habilidad,
                "indice": i
            })
            
            # Diseño del botón de habilidad
            pygame.draw.rect(ventana, self.c.BLANCO, rect_boton, border_radius=15)
            pygame.draw.rect(ventana, self.c.NEON, rect_boton, 3, border_radius=15)
            
            # Texto centrado en el botón
            txt_hab = self.c.f_chica.render(habilidad, True, self.c.BLANCO)
            txt_rect = txt_hab.get_rect(center=rect_boton.center)
            ventana.blit(txt_hab, txt_rect)