import pygame
import os

class Estructura_Vista:
    def __init__(self, config):
        self.c = config
        self.botones_evolucion = []
        
        # Coordenadas del mapa (Grafo)
        self.posiciones_mapa = {
            "Inicio": (820, 520),
            "Campus": (750, 410),
            "Comedor": (890, 410),
            "Ed39": (820, 300),
            "Piso 5": (820, 150)
        }
        
        # Ruta base del proyecto
        self.ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def dibujar_mapa_grafo(self, ventana, modelo):
        """Dibuja SOLO el mapa. Las vidas solo aparecen en combate."""
        # 1. Lineas de conexion (Aristas)
        for origen, destinos in modelo.encuentros.grafo_mapa.items():
            for destino in destinos:
                if origen in self.posiciones_mapa and destino in self.posiciones_mapa:
                    pygame.draw.line(ventana, self.c.AZUL, self.posiciones_mapa[origen], self.posiciones_mapa[destino], 4)

        jugador = modelo.obtener_jugador_actual()
        
        # 2. Nodos del mapa con letra pequena (tipo Arial)
        for nodo, pos in self.posiciones_mapa.items():
            es_actual = (nodo == jugador.nodo_actual)
            color_nodo = self.c.NEON if es_actual else (60, 60, 60)
            
            pygame.draw.circle(ventana, color_nodo, pos, 25)
            pygame.draw.circle(ventana, self.c.BLANCO, pos, 25, 2)
            
            # Texto centrado debajo del nodo
            txt_nodo = self.c.f_chica.render(nodo, True, self.c.BLANCO)
            rect_txt = txt_nodo.get_rect(center=(pos[0], pos[1] + 45))
            ventana.blit(txt_nodo, rect_txt)


    def dibujar_arbol_habilidades(self, ventana, modelo):
        """Pantalla de seleccion de evolucion"""
        try:
            ruta_img = os.path.join(self.ruta_proyecto, "Imagenes", "Fondo_Habilidad.png")
            fondo = pygame.image.load(ruta_img)
            ventana.blit(pygame.transform.scale(fondo, (930, 600)), (0, 0))
        except:
            ventana.fill((40, 40, 50))

        self.botones_evolucion = []
        opciones = modelo.evolucionar_jugador()

        # Titulo Level Up
        txt_t = "¡LEVEL UP!"
        tit_frente = self.c.f_grande.render(txt_t, True, self.c.NEON)
        ventana.blit(tit_frente, (465 - tit_frente.get_width()//2, 50))

        # Botones de evolucion (f_chica para que no se deformen)
        for i, habilidad in enumerate(opciones):
            rect_b = pygame.Rect(200 + (i * 350), 475, 220, 80)
            self.botones_evolucion.append({"rect": rect_b, "habilidad": habilidad, "indice": i})
            
            pygame.draw.rect(ventana, self.c.BLANCO, rect_b, border_radius=15)
            pygame.draw.rect(ventana, self.c.NEON, rect_b, 3, border_radius=15)
            
            txt_hab = self.c.f_chica.render(habilidad, True, self.c.NEGRO)
            ventana.blit(txt_hab, txt_hab.get_rect(center=rect_b.center))

    def dibujar_pantalla_muerte(self, ventana, modelo, mensaje=""):
        """Pantalla de derrota"""
        overlay = pygame.Surface((930, 600), pygame.SRCALPHA)
        overlay.fill((20, 0, 0, 215)) 
        ventana.blit(overlay, (0, 0))

        jugador = modelo.obtener_jugador_actual()
        
        frente = self.c.f_grande.render("FALLO ACADEMICO", True, (255, 80, 0))
        ventana.blit(frente, (465 - frente.get_width()//2, 180))

        txt_msg = self.c.f_chica.render(mensaje.upper(), True, (255, 255, 255))
        ventana.blit(txt_msg, (465 - txt_msg.get_width()//2, 280))

        self.rect_boton_muerte = pygame.Rect(315, 410, 300, 60)
        msg_btn = "ESTUDIAR MAS" if jugador.vidas > 0 else "ANULAR MATRICULA"
        
        pygame.draw.rect(ventana, (30, 30, 30), self.rect_boton_muerte, border_radius=12)
        txt_b = self.c.f_chica.render(msg_btn, True, (255, 255, 255))
        ventana.blit(txt_b, txt_b.get_rect(center=self.rect_boton_muerte.center))