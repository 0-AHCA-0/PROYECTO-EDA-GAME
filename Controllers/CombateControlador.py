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
        Inicializa el controlador de combate sincronizando LPs con la vista.
        """
        self.modelo = modelo
        self.vista = vista
        self.jugador = modelo.obtener_jugador_actual()
        
        self.jugador.vidas_max = self.jugador.vida_max 
        
        # Crear enemigo con dificultad basada en el nivel del jugador
        dificultad = max(1, self.jugador.nivel_evolucion)
        self.enemigo = Enemy("Enemigo", dificultad)
        
        # El enemigo también debe tener sincronizada su vida máxima para su barra
        self.enemigo.vida = 50 * dificultad
        self.enemigo.vidas_max = self.enemigo.vida  
        
        self.log_daño = "¡Un enemigo aparece! Prepárate."
        self.combate_activo = True
    
    def ejecutar(self, eventos):
        """
        Procesa los eventos del combate.
        """
        # 1. SI EL COMBATE TERMINÓ: Esperamos un clic para salir al estado correspondiente
        if not self.combate_activo:
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    return self._obtener_estado_final()
            return "COMBATE"
        
        # 2. DURANTE EL COMBATE: Procesar ataques
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Detección de clic en el botón de habilidad definido en la vista
                if self.vista.rect_boton_hab.collidepoint(evento.pos):
                    return self._logica_ataque()
        
        return "COMBATE"
    
    def _logica_ataque(self):
        """
        Lógica de combate: Se restan LPs. 
        Si llega a 0, se descuenta una Vida Global.
        """
        # 1. ATAQUE DEL JUGADOR
        danio_jugador = self.jugador.dano 
        self.enemigo.vida -= danio_jugador
        self.log_daño = f"¡{self.jugador.habilidad_actual} causó {danio_jugador} LP de daño!"
        
        # 2. VERIFICAR VICTORIA
        if self.enemigo.vida <= 0:
            self.enemigo.vida = 0
            self.log_daño = "¡VICTORIA! Haz clic para continuar."
            self.combate_activo = False
            return "COMBATE"
        
        # 3. CONTRAATAQUE DEL ENEMIGO
        # El enemigo hace daño numérico (ej: 15 LP)
        daño_enemigo = self.enemigo.dano
        self.jugador.vida -= daño_enemigo
        self.log_daño += f" | {self.enemigo.nombre} te quitó {daño_enemigo} LP"
        
        # 4. VERIFICAR DERROTA (Si los LPs llegan a 0)
        if self.jugador.vida <= 0:
            self.jugador.vidas -= 1       # Pierde 1 de las 3 vidas globales
            self.jugador.vida = self.jugador.vida_max # Reset LPs para el siguiente intento
            self.combate_activo = False
            
            if self.jugador.vidas <= 0:
                self.jugador.vidas = 0
                self.jugador.vivo = False
                self.log_daño = "¡DERROTA TOTAL! Has perdido todas tus vidas."
            else:
                self.log_daño = f"¡HAS CAÍDO! Te quedan {self.jugador.vidas} vidas globales."
            
            return "COMBATE" 
        
        return "COMBATE"
    
    def _obtener_estado_final(self):
        """
        Retorna el estado al que debe cambiar el Main.
        """
        if self.jugador.vivo:
            return "JUEGO" # Regresa al mapa si ganó
        else:

            return "PANTALLA_MUERTE" 

    def obtener_log(self):
        return self.log_daño

    def obtener_enemigo(self):
        return self.enemigo