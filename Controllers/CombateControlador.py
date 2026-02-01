import pygame
from Models.Entidades import Enemy
from Models.Entidades import Player

class CombateControlador:
    """
    Controlador de combate por turnos.
    Gestiona la lógica de batalla entre un jugador y un enemigo.
    """
    
    def __init__(self, modelo, vista):
        """
        Inicializa el controlador de combate.
        """
        self.modelo = modelo
        self.vista = vista
        self.jugador = modelo.obtener_jugador_actual()
        
        # Sincronizamos vidas máximas para la barra de la vista
        self.jugador.vidas_max = 5
        
        # Crear enemigo con dificultad basada en el nivel del jugador
        dificultad = max(1, self.jugador.nivel_evolucion)
        self.enemigo = Enemy("Enemigo", dificultad)
        
        # Ajustamos la vida del enemigo para que el combate dure (ej: 50 HP)
        self.enemigo.vida = 50 * dificultad
        self.enemigo.vidas_max = self.enemigo.vida  
        
        # Log de combate
        self.log_daño = "¡Un enemigo aparece! Prepárate."
        self.combate_activo = True
    
    def ejecutar(self, eventos):
        """
        Procesa los eventos del combate.
        """
        # Si el combate ya terminó (victoria o derrota), esperamos un clic para salir
        if not self.combate_activo:
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    return self._obtener_estado_final()
            return "COMBATE"
        
        # Lógica de interacción durante el combate
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Detección de clic en el botón de habilidad definido en la vista
                if self.vista.rect_boton_hab.collidepoint(evento.pos):
                    return self._logica_ataque()
        
        return "COMBATE"
    
    def _logica_ataque(self):
        """
        Ejecuta la lógica de ataque del jugador y contraataque enemigo.
        """
        # 1. ATAQUE DEL JUGADOR
        # Bajamos el daño a 10 para que el enemigo de 50 HP dure 5 turnos
        daño_jugador = 10 
        self.enemigo.vida -= daño_jugador
        
        # Actualizamos el log para que el usuario vea qué pasó
        self.log_daño = f"¡{self.jugador.habilidad_actual} causó {daño_jugador} de daño!"
        
        # 2. VERIFICAR VICTORIA
        if self.enemigo.vida <= 0:
            self.enemigo.vida = 0
            self.log_daño = "¡VICTORIA! Haz clic en cualquier lugar para continuar."
            self.combate_activo = False
            return "COMBATE" # No salimos todavía para que se lea el log
        
        # 3. CONTRAATAQUE DEL ENEMIGO
        # El enemigo quita 1 vida (un corazón)
        self.jugador.vidas -= 1
        self.log_daño += f" | {self.enemigo.nombre} te quitó 1 corazón"
        
        # 4. VERIFICAR DERROTA
        if self.jugador.vidas <= 0:
            self.jugador.vidas = 0
            self.jugador.vivo = False
            self.combate_activo = False
            # Al ser derrota, el Main nos llevará a la pantalla de Game Over tras el clic
            return "COMBATE" 
        
        return "COMBATE"
    
    def _obtener_estado_final(self):
        """Retorna el estado al que debe cambiar el Main."""
        if self.jugador.vivo:
            return "JUEGO" # Regresa al mapa
        else:
            return "DERROTA" # Va a pantalla de Game Over

    def obtener_log(self):
        return self.log_daño

    def obtener_enemigo(self):
        return self.enemigo