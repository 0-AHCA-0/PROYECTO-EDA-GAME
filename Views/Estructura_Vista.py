import pygame
import os

class Estructura_Vista:
    def __init__(self, config):
        self.c = config
        self.botones_evolucion = []  # Almacena los Rect de los botones
        
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
        """Renderiza el Grafo Dirigido de rutas del juego"""
        for origen, destinos in modelo.encuentros.grafo_mapa.items():
            for destino in destinos:
                if origen in self.posiciones_mapa and destino in self.posiciones_mapa:
                    pygame.draw.line(ventana, self.c.AZUL, self.posiciones_mapa[origen], self.posiciones_mapa[destino], 4)

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
        Pantalla de evolución con el fondo correcto.
        """
        # 1. CARGAR EL FONDO (Soporte para .jpg y .png por si acaso)
        imagen_cargada = False
        nombres_posibles = ["Fondo_Habilidad.jpg", "Fondo_Habilidad.png"] 
        
        for nombre in nombres_posibles:
            try:
                ruta_img = os.path.join(self.ruta_proyecto, "Imagenes", nombre)
                if os.path.exists(ruta_img):
                    fondo = pygame.image.load(ruta_img)
                    fondo = pygame.transform.scale(fondo, (930, 600))
                    ventana.blit(fondo, (0, 0))
                    imagen_cargada = True
                    break
            except:
                continue

        if not imagen_cargada:
            ventana.fill((50, 50, 60)) # Respaldo gris si no encuentra nada

        # 2. Limpiar botones previos
        self.botones_evolucion = []

        opciones = modelo.evolucionar_jugador()

        # 3. TÍTULO CORREGIDO (Centrado y con color)
        texto_titulo = "¡LEVEL UP!"
        
        # Capa de sombra (Negro)
        titulo_sombra = self.c.f_grande.render(texto_titulo, True, self.c.NEGRO)
        # Capa principal (Neón)
        titulo = self.c.f_grande.render(texto_titulo, True, self.c.NEON)
        
        # Calculamos el centro horizontal
        ancho_pantalla = 930
        ancho_texto = titulo.get_width()
        x_centrada = (ancho_pantalla - ancho_texto) // 2
        
        # --- AQUÍ ESTABA EL ERROR ---
        # Primero dibujamos la sombra desplazada (+3 px)
        ventana.blit(titulo_sombra, (x_centrada + 3, 53))
        # Y LUEGO dibujamos el texto de neón encima
        ventana.blit(titulo, (x_centrada, 50))

        # 4. Dibujar botones
        for i, habilidad in enumerate(opciones):
            x_pos = 200 + (i * 350)
            rect_boton = pygame.Rect(x_pos, 475, 220, 80)
            
            self.botones_evolucion.append({
                "rect": rect_boton,
                "habilidad": habilidad,
                "indice": i
            })
            
            # Botón Blanco
            pygame.draw.rect(ventana, self.c.BLANCO, rect_boton, border_radius=15)
            # Borde Neón
            pygame.draw.rect(ventana, self.c.NEON, rect_boton, 3, border_radius=15)
            
            # Texto Negro
            txt_hab = self.c.f_chica.render(habilidad, True, self.c.NEGRO)
            txt_rect = txt_hab.get_rect(center=rect_boton.center)
            ventana.blit(txt_hab, txt_rect)
    


    # --- AGREGAR A Estructura_Vista.py ---

    def dibujar_pantalla_muerte(self, ventana, modelo):
        """Pantalla de transición cuando un jugador muere"""
        # 1. Overlay oscuro (930x600 según tu Main)
        overlay = pygame.Surface((930, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190)) 
        ventana.blit(overlay, (0, 0))

        jugador = modelo.obtener_jugador_actual()
        hay_vivos = modelo.verificar_sobrevivientes()
        
        # 2. Título con sombra (Estilo Leyendas Elementales)
        txt = f"¡{jugador.nombre.upper()} HA CAÍDO!"
        sombra = self.c.f_grande.render(txt, True, self.c.NEGRO)
        frente = self.c.f_grande.render(txt, True, (255, 50, 50)) # Rojo
        
        x_tit = (930 - frente.get_width()) // 2
        ventana.blit(sombra, (x_tit + 3, 153))
        ventana.blit(frente, (x_tit, 150))

        # 3. Botón de Relevo / Reinicio
        # Guardamos el rect para que el Main detecte el clic
        self.rect_boton_muerte = pygame.Rect(315, 350, 300, 65)
        
        if modelo.modo_juego == 2 and hay_vivos:
            msg_btn = "TURNO DEL COMPAÑERO"
            color_borde = self.c.NEON
        else:
            msg_btn = "VOLVER AL MENÚ"
            color_borde = (200, 50, 50)

        # Dibujo con bordes redondeados (como tus otros botones)
        pygame.draw.rect(ventana, self.c.BLANCO, self.rect_boton_muerte, border_radius=12)
        pygame.draw.rect(ventana, color_borde, self.rect_boton_muerte, 4, border_radius=12)
        
        txt_btn = self.c.f_chica.render(msg_btn, True, self.c.NEGRO)
        ventana.blit(txt_btn, (self.rect_boton_muerte.centerx - txt_btn.get_width()//2, 
                            self.rect_boton_muerte.centery - txt_btn.get_height()//2))