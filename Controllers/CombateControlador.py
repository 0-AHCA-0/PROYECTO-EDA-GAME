import pygame
from Models.Entidades import Enemy

class CombateControlador:
    """
    Controlador de combate por turnos.
    Permite que el jugador siga luchando mientras tenga vidas globales (corazones).
    """
    
    def __init__(self, modelo, vista):
        # Vinculacion con el modelo y la vista para procesar datos y graficos
        self.modelo = modelo
        self.vista = vista
        self.jugador = modelo.obtener_jugador_actual()
        
        # 1. IDENTIFICACION DEL RIVAL
        # Si el jugador esta parado en el Piso 5, el enemigo es Boris (Jefe Final)
        es_jefe = getattr(self.jugador, "nodo_actual", "") == "Piso 5"
        nombre_e = "Boris" if es_jefe else "Guardia"
        
        # La fuerza del enemigo escala proporcionalmente al nivel del jugador
        dificultad = max(1, self.jugador.nivel_evolucion)
        
        # 2. CREACION DE LA ENTIDAD ENEMIGA
        # Se genera el objeto y se registra en el modelo para que la vista lo dibuje
        self.enemigo = Enemy(nombre_e, dificultad)
        self.modelo.encuentros.enemigo_actual = self.enemigo
        
        # Variables de control de flujo y log de batalla
        self.log_daño = f"Un {nombre_e} aparece!"
        self.combate_activo = True
        self.victoria = False
        self.derrota = False
        
        #Musica 
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        try:
            if es_jefe:
                pygame.mixer.music.load("Audio/intro_boris.mp3")
                segundo_inicio = 21.0
                
            else:
                pygame.mixer.music.load("Audio/Enemy_8bits.mp3")
                segundo_inicio = 0.00
            
            pygame.mixer.music.play(loops=-1, start=segundo_inicio)
            pygame.mixer.music.set_volume(0.9)
        except:
            print("No se encontro nada")

    def ejecutar(self, eventos):
        """
        Bucle de logica de combate. Gestiona ataques y cambios de estado.
        """
        # Si la pelea termino, el sistema espera un clic para volver al mapa o morir
        if not self.combate_activo:
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    return self._obtener_estado_final()
            return "COMBATE"

        # Turno del Jugador: Detectar clic sobre el boton de ataque/habilidad
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.vista.rect_boton_hab.collidepoint(evento.pos):
                    self._procesar_turno_jugador()
        
        return "COMBATE"

    def _procesar_turno_jugador(self):
        """
        Calcula el intercambio de dano entre el jugador y el oponente.
        """
        # 1. ATAQUE DEL JUGADOR
        # Se resta el dano de la habilidad actual a la vida del enemigo
        daño_j = self.jugador.dano
        self.enemigo.vida -= daño_j
        self.log_daño = f"Usaste {self.jugador.habilidad_actual}: -{daño_j} HP al enemigo"

        # Verificacion de victoria: si el enemigo llega a 0 se detiene el combate
        if self.enemigo.vida <= 0:
            self.enemigo.vida = 0
            self.log_daño = "Enemigo derrotado! Puedes continuar."
            self.combate_activo = False
            self.victoria = True
            return

        # 2. TURNO DEL ENEMIGO (CONTRAATAQUE)
        # El enemigo responde de inmediato si sobrevivio al golpe
        daño_e = self.enemigo.dano
        self.jugador.vida -= daño_e
        self.log_daño += f" | El enemigo te quito {daño_e} LP"

        # --- LOGICA DE RESURRECCION POR VIDAS (CORAZONES) ---
        # Si la barra de vida llega a cero, se consume un corazon global
        if self.jugador.vida <= 0:
            self.jugador.vidas -= 1 
            
            if self.jugador.vidas > 0:
                # El jugador aun tiene intentos: recupera vida y sigue la pelea
                self.jugador.vida = self.jugador.vida_max
                self.log_daño = f"Caiste! Pero usas una vida extra. Te quedan {self.jugador.vidas}"
            else:
                # Se agotaron todas las oportunidades: derrota definitiva
                self.jugador.vida = 0
                self.combate_activo = False
                self.derrota = True
                self.log_daño = "DERROTA TOTAL! Has reprobado todas tus oportunidades."

    def _obtener_estado_final(self):
        """
        Determina a que pantalla enviar al jugador tras finalizar el combate.
        """
        #Primero, antes de salir del combate detenemos la musica
        pygame.mixer.music.stop()
        
        #Determinar estado
        if self.victoria:
            # Ganas XP y el sistema revisa si subes de nivel (Estado EVOLUCION)
            subio = self.jugador.ganar_xp(40)
            return "EVOLUCION" if subio else "JUEGO"
        
        if self.derrota:
            # Activa la pantalla de muerte personalizada guardada en el Maestro
            return "PANTALLA_MUERTE"
            
        return "JUEGO"