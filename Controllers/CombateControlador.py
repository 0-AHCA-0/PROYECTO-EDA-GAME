import pygame
from Models.Entidades import Enemy

class CombateControlador:
    """
    Controlador de combate por turnos.
    Gestiona la lógica de batalla entre un jugador y un enemigo.
    """
    
    def __init__(self, modelo, vista):
        """
        Inicializa el combate y vincula al enemigo con el modelo para que la vista lo vea.
        """
        self.modelo = modelo
        self.vista = vista
        self.jugador = modelo.obtener_jugador_actual()
        
        # 1. Crear enemigo basado en el nivel del jugador
        dificultad = max(1, self.jugador.nivel_evolucion)
        self.enemigo = Enemy("Enemigo", dificultad)
        
        # Sincronizar vida máxima para la barra de la vista
        self.enemigo.vida_max = 50 * dificultad
        self.enemigo.vida = self.enemigo.vida_max
        
        # 2. VINCULACIÓN CRÍTICA: Guardamos el enemigo en el modelo
        # Esto permite que la vista lo encuentre al hacer: modelo.encuentros.enemigo_actual
        self.modelo.encuentros.enemigo_actual = self.enemigo
        
        self.log_daño = "¡Un enemigo aparece! Prepárate."
        self.combate_activo = True
        self.victoria = False
        self.derrota = False

    def ejecutar(self, eventos):
        """
        Procesa los eventos del combate.
        """
        # Si el combate ya terminó, esperamos un clic para transicionar de estado
        if not self.combate_activo:
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    # Limpiamos el enemigo del modelo al salir para liberar memoria
                    self.modelo.encuentros.enemigo_actual = None
                    return self._obtener_estado_final()
            return "COMBATE"
        
        # Procesar ataque si el jugador hace clic en el botón de habilidad
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.vista.rect_boton_hab.collidepoint(evento.pos):
                    return self._logica_ataque()
        
        return "COMBATE"
    
    def _logica_ataque(self):
        """
        Lógica de intercambio de daño.
        """
        # 1. TURNO DEL JUGADOR
        danio_jugador = self.jugador.dano 
        self.enemigo.vida -= danio_jugador
        self.log_daño = f"¡{self.jugador.habilidad_actual} causó {danio_jugador} de daño!"
        
        # Verificar si el enemigo murió
        if self.enemigo.vida <= 0:
            self.enemigo.vida = 0
            self.log_daño = "¡VICTORIA! Haz clic para continuar."
            self.combate_activo = False
            self.victoria = True
            return "COMBATE"
        
        # 2. TURNO DEL ENEMIGO (Contraataque)
        daño_enemigo = self.enemigo.dano
        self.jugador.vida -= daño_enemigo
        self.log_daño += f" | El enemigo te quitó {daño_enemigo} HP"
        
        # Verificar si el jugador murió (HP llega a 0)
        if self.jugador.vida <= 0:
            self.jugador.vida = 0
            self.jugador.vidas -= 1  # Restar vida global
            self.combate_activo = False
            self.derrota = True
            
            if self.jugador.vidas <= 0:
                self.log_daño = "¡DERROTA TOTAL! Has perdido todas tus vidas."
            else:
                self.log_daño = f"¡HAS CAÍDO! Te quedan {self.jugador.vidas} vidas globales."
            
            return "COMBATE" 
        
        return "COMBATE"
    
    def _obtener_estado_final(self):
        """
        Determina a qué estado debe ir el ControladorMaestro al cerrar el combate.
        """
        if self.victoria:
            # Gana XP y verifica si sube de nivel (evolución)
            subio = self.jugador.ganar_xp(30)
            return "EVOLUCION" if subio else "JUEGO"
        
        if self.derrota:
            # Si perdió, el HP se resetea para que pueda seguir jugando si le quedan vidas
            self.jugador.vida = self.jugador.vida_max
            return "PANTALLA_MUERTE"
        
        return "JUEGO"

    def obtener_log(self):
        return self.log_daño