import pygame
import os

class Estructura_Vista:
    def __init__(self, config):
        self.c = config
        self.botones_evolucion = []  # Almacena los Rect de los botones
        
        # Coordenadas del mapa (Grafo)
        self.posiciones_mapa = {
            "Inicio": (750, 500),
            "Campus": (650, 380),
            "Comedor": (850, 380),
            "Ed39": (750, 250),
            "Piso 5": (750, 100)
        }
        
        # Localizamos la ruta del proyecto una sola vez
        self.ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def dibujar_mapa_grafo(self, ventana, modelo):
        """Renderiza el Grafo Dirigido de rutas del juego"""
        # 1. Dibujar Aristas
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

        # 2. Dibujar Nodos
        jugador = modelo.obtener_jugador_actual()
        for nodo, pos in self.posiciones_mapa.items():
            es_actual = (nodo == jugador.nodo_actual)
            color_nodo = self.c.NEON if es_actual else (60, 60, 60)
            
            pygame.draw.circle(ventana, color_nodo, pos, 25)
            pygame.draw.circle(ventana, self.c.BLANCO, pos, 25, 2)
            
            txt_nodo = self.c.f_chica.render(nodo, True, self.c.BLANCO)
            ventana.blit(txt_nodo, (pos[0] - 25, pos[1] + 30))

    def dibujar_arbol_habilidades(self, ventana, modelo, ruta_fondo=None):
        """
        Pantalla de evolución con fondo de Elmo forzado.
        """
        # 1. FORZAR FONDO DE ELMO
        # Intentamos cargar a Elmo directamente aquí para asegurar que se vea
        try:
            ruta_img_fondo = os.path.join(self.ruta_proyecto, "Imagenes", "Elmo_Fondo.png")
            fondo = pygame.image.load(ruta_img_fondo)
            fondo = pygame.transform.scale(fondo, (930, 600))
            ventana.blit(fondo, (0, 0))
        except Exception as e:
            # Si falla, usamos un gris oscuro, pero NO negro total
            ventana.fill((50, 50, 60))

        # 2. Limpiar botones previos
        self.botones_evolucion = []

        opciones = modelo.evolucionar_jugador()

        # 3. Título principal
        # Usamos una sombra negra pequeña para que se lea bien sobre Elmo
        titulo_sombra = self.c.f_grande.render("¡NUEVA HABILIDAD DISPONIBLE!", True, self.c.NEGRO)
        titulo = self.c.f_grande.render("¡NUEVA HABILIDAD DISPONIBLE!", True, self.c.NEON)
        ventana.blit(titulo_sombra, (152, 102))
        ventana.blit(titulo, (150, 100))

        # 4. Dibujar botones
        for i, habilidad in enumerate(opciones):
            x_pos = 200 + (i * 350)
            rect_boton = pygame.Rect(x_pos, 300, 220, 80)
            
            self.botones_evolucion.append({
                "rect": rect_boton,
                "habilidad": habilidad,
                "indice": i
            })
            
            # Botón Blanco
            pygame.draw.rect(ventana, self.c.BLANCO, rect_boton, border_radius=15)
            # Borde Neón
            pygame.draw.rect(ventana, self.c.NEON, rect_boton, 3, border_radius=15)
            
            # --- CORRECCIÓN CRÍTICA DE COLOR ---
            # Antes tenías self.c.BLANCO (texto blanco sobre botón blanco = invisible)
            # Ahora usamos self.c.NEGRO
            txt_hab = self.c.f_chica.render(habilidad, True, self.c.NEGRO) 
            
            txt_rect = txt_hab.get_rect(center=rect_boton.center)
            ventana.blit(txt_hab, txt_rect)