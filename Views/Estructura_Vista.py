import pygame
import os

# Esta clase dibuja el esqueleto del juego: Mapa, Evoluciones y Derrota
class Estructura_Vista:
    def __init__(self, config):
        self.c = config
        self.botones_evolucion = [] # Lista para saber donde estan los botones de nivel
        
        # COORDENADAS: Aqui defines donde aparece cada circulo en la pantalla
        self.posiciones_mapa = {
            "Inicio": (820, 520),
            "Campus": (750, 410),
            "Comedor": (890, 410),
            "Ed39": (820, 300),
            "Piso 5": (820, 150)
        }
        
        # Busca la carpeta raiz para encontrar las imagenes de fondo
        self.ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def dibujar_mapa_grafo(self, ventana, modelo):
        """Dibuja las lineas y circulos del mapa"""
        # 1. DIBUJAR LINEAS: Conecta los lugares segun el Sistema de Encuentros
        for origen, destinos in modelo.encuentros.grafo_mapa.items():
            for destino in destinos:
                if origen in self.posiciones_mapa and destino in self.posiciones_mapa:
                    pygame.draw.line(ventana, self.c.AZUL, self.posiciones_mapa[origen], self.posiciones_mapa[destino], 4)

        jugador = modelo.obtener_jugador_actual()
        
        # 2. DIBUJAR NODOS: Los circulos donde haces clic para moverte
        for nodo, pos in self.posiciones_mapa.items():
            # Si el jugador esta parado aqui, el circulo brilla en color NEON
            es_actual = (nodo == jugador.nodo_actual)
            color_nodo = self.c.NEON if es_actual else (60, 60, 60)
            
            pygame.draw.circle(ventana, color_nodo, pos, 25)
            pygame.draw.circle(ventana, self.c.BLANCO, pos, 25, 2)
            
            # Nombre del lugar debajo del circulo
            txt_nodo = self.c.f_chica.render(nodo, True, self.c.BLANCO)
            rect_txt = txt_nodo.get_rect(center=(pos[0], pos[1] + 45))
            ventana.blit(txt_nodo, rect_txt)


    def dibujar_arbol_habilidades(self, ventana, modelo):
        """Dibuja la pantalla de seleccion cuando subes de nivel"""
        try:
            # Intenta cargar el fondo de evolucion
            ruta_img = os.path.join(self.ruta_proyecto, "Imagenes", "Fondo_Habilidad.png")
            fondo = pygame.image.load(ruta_img)
            ventana.blit(pygame.transform.scale(fondo, (930, 600)), (0, 0))
        except:
            ventana.fill((40, 40, 50))

        self.botones_evolucion = [] # Limpia la lista de botones anteriores
        opciones = modelo.evolucionar_jugador() # Pregunta al modelo que ataques puede elegir

        # Titulo brillante
        txt_t = "LEVEL UP!"
        tit_frente = self.c.f_grande.render(txt_t, True, self.c.NEON)
        ventana.blit(tit_frente, (465 - tit_frente.get_width()//2, 50))

        # Crea los botones para cada opcion de ataque nueva
        for i, habilidad in enumerate(opciones):
            rect_b = pygame.Rect(200 + (i * 350), 475, 220, 80)
            # Guarda el rectangulo para que el controlador detecte el clic
            self.botones_evolucion.append({"rect": rect_b, "habilidad": habilidad, "indice": i})
            
            pygame.draw.rect(ventana, self.c.BLANCO, rect_b, border_radius=15)
            pygame.draw.rect(ventana, self.c.NEON, rect_b, 3, border_radius=15)
            
            txt_hab = self.c.f_chica.render(habilidad, True, self.c.NEGRO)
            ventana.blit(txt_hab, txt_hab.get_rect(center=rect_b.center))

    def dibujar_pantalla_muerte(self, ventana, modelo, mensaje="", titulo="FALLO ACADEMICO"):
        """Pantalla de derrota: Muestra el fin de la partida por diferentes motivos."""
        
        # 1. CREAR EL AMBIENTE DE DERROTA
        # Generamos una capa roja semi-transparente para oscurecer el fondo del juego
        overlay = pygame.Surface((930, 600), pygame.SRCALPHA)
        overlay.fill((30, 0, 0, 220)) # Un rojo oscuro para dar sensacion de peligro
        ventana.blit(overlay, (0, 0))

        # Obtenemos los datos del jugador para saber cuantas vidas globales le quedan
        jugador = modelo.obtener_jugador_actual()
        
        # 2. TITULO DINAMICO 
        # Renderiza el titulo que viene del controlador 
        # Se usa .upper() para que siempre salga en mayusculas imponentes
        frente = self.c.f_grande.render(titulo.upper(), True, (255, 80, 0))
        # Se centra horizontalmente restando la mitad del ancho del texto al centro de la pantalla 
        ventana.blit(frente, (465 - frente.get_width()//2, 180))

        # 3. MENSAJE DE DETALLE 
        # Aqui se muestra el texto largo (ej: 
        txt_msg = self.c.f_chica.render(mensaje.upper(), True, (255, 255, 255))
        ventana.blit(txt_msg, (465 - txt_msg.get_width()//2, 280))

        # 4. BOTON DE ACCION (ESTUDIAR O RENUNCIAR)
        # Definimos el area interactiva del boton
        self.rect_boton_muerte = pygame.Rect(315, 410, 300, 60)
        
        # Si al jugador aun le quedan vidas (corazones), puede reintentar (Estudiar mas)
        # Si ya perdio todo, el juego le obliga a salir (Anular matricula)
        msg_btn = "ESTUDIAR MAS" if jugador.vidas > 0 else "ANULAR MATRICULA"
        
        # Dibujamos el cuerpo del boton en gris oscuro
        pygame.draw.rect(ventana, (40, 40, 40), self.rect_boton_muerte, border_radius=12)
        
        # Escribimos el texto del boton centrado exactamente en su rectangulo
        txt_b = self.c.f_chica.render(msg_btn, True, (255, 255, 255))
        ventana.blit(txt_b, txt_b.get_rect(center=self.rect_boton_muerte.center))