import pygame
from Models.Entidades import Enemy


class CombateControlador:
    """
    Controlador de combate por turnos.
    Gestiona la lógica de batalla entre un jugador y un enemigo.
    """
    
    def __init__(self, modelo, vista):
        """
        Inicializa el controlador de combate.
        
        Args:
            modelo: Instancia de GameModel con los jugadores.
            vista: Instancia de Combate_Vista para renderizar.
        """
        self.modelo = modelo
        self.vista = vista
        self.jugador = modelo.obtener_jugador_actual()
        
        # Crear enemigo con dificultad basada en el nivel del jugador
        dificultad = max(1, self.jugador.nivel_evolucion)
        self.enemigo = Enemy("Enemigo", dificultad)
        self.enemigo.vidas_max = self.enemigo.vida  # Para la barra de vida
        
        # Log de combate
        self.log_daño = "Inicia el combate..."
        self.combate_activo = True
    
    def ejecutar(self, eventos):
        """
        Procesa los eventos del combate.
        
        Args:
            eventos: Lista de eventos de Pygame.
            
        Returns:
            str: "JUEGO" para volver al mapa, "DERROTA" si el jugador muere,
                 "COMBATE" para continuar el combate.
        """
        if not self.combate_activo:
            return self._obtener_estado_final()
        
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Detección de clic en el botón de habilidad
                if self.vista.rect_boton_hab.collidepoint(evento.pos):
                    return self._procesar_ataque()
        
        return "COMBATE"
    
    def _procesar_ataque(self):
        """
        Ejecuta la lógica de ataque del jugador.
        
        Returns:
            str: "JUEGO" si el enemigo muere, "DERROTA" si el jugador muere,
                 "COMBATE" para continuar.
        """
        # Calcular daño con variación
        daño = self.jugador.dano
        self.enemigo.vida -= daño
        
        # Log del ataque
        self.log_daño = f"Usaste {self.jugador.habilidad_actual} y causaste {daño} de daño"
        
        # Verificar si el enemigo murió
        if self.enemigo.vida <= 0:
            self.combate_activo = False
            self.log_daño = f"¡{self.enemigo.nombre} fue derrotado!"
            return "JUEGO"
        
        # Contraataque del enemigo
        daño_enemigo = self.enemigo.dano
        self.jugador.vidas -= 1
        self.log_daño += f" | {self.enemigo.nombre} te atacó y perdiste 1 vida"
        
        # Verificar si el jugador murió
        if self.jugador.vidas <= 0:
            self.jugador.vivo = False
            self.combate_activo = False
            return "DERROTA"
        
        return "COMBATE"
    
    def _obtener_estado_final(self):
        """
        Retorna el estado final del combate.
        
        Returns:
            str: "JUEGO" o "DERROTA" según el resultado.
        """
        if self.jugador.vivo:
            return "JUEGO"
        else:
            return "DERROTA"
    
    def obtener_log(self):
        """Retorna el log actual de combate."""
        return self.log_daño
    
    def obtener_enemigo(self):
        """Retorna la referencia al enemigo."""
        return self.enemigo
