import pygame
from Models.Entidades import Enemy

class CombateControlador:
    """
    Controlador de combate por turnos.
    Permite que el jugador siga luchando mientras tenga vidas globales.
    """
    
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self.jugador = modelo.obtener_jugador_actual()
        
        # 1. Determinamos si es Boris (Jefe final) o un guardia normal
        es_jefe = getattr(self.jugador, "nodo_actual", "") == "Piso 5"
        nombre_e = "Boris" if es_jefe else "Guardia"
        
        # Dificultad basada en la evolucion del jugador
        dificultad = max(1, self.jugador.nivel_evolucion)
        
        # 2. Creamos al enemigo y lo vinculamos al modelo para la vista
        self.enemigo = Enemy(nombre_e, dificultad)
        self.modelo.encuentros.enemigo_actual = self.enemigo
        
        self.log_daño = f"¡Un {nombre_e} aparece!"
        self.combate_activo = True
        self.victoria = False
        self.derrota = False

    def ejecutar(self, eventos):
        """
        Bucle de logica del combate.
        """
        # Si la pelea termino, esperamos un clic para salir al mapa o pantalla de muerte
        if not self.combate_activo:
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    return self._obtener_estado_final()
            return "COMBATE"

        # Turno del Jugador: Detectar clic en el boton de habilidad
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.vista.rect_boton_hab.collidepoint(evento.pos):
                    self._procesar_turno_jugador()
        
        return "COMBATE"

    def _procesar_turno_jugador(self):
        # 1. ATAQUE DEL JUGADOR
        daño_j = self.jugador.dano
        self.enemigo.vida -= daño_j
        self.log_daño = f"Usaste {self.jugador.habilidad_actual}: -{daño_j} HP al enemigo"

        # Verificar si el enemigo murio
        if self.enemigo.vida <= 0:
            self.enemigo.vida = 0
            self.log_daño = "¡Enemigo derrotado! Puedes continuar."
            self.combate_activo = False
            self.victoria = True
            return

        # 2. TURNO DEL ENEMIGO (Contraataque inmediato)
        daño_e = self.enemigo.dano
        self.jugador.vida -= daño_e
        self.log_daño += f" | El enemigo te quito {daño_e} LP"

        # --- LOGICA DE VIDA CONTINUA ---
        if self.jugador.vida <= 0:
            self.jugador.vidas -= 1 # Restamos una vida global (corazon)
            
            if self.jugador.vidas > 0:
                # El jugador aun tiene repuestos: se cura y sigue la pelea
                self.jugador.vida = self.jugador.vida_max
                self.log_daño = f"¡Caiste! Pero usas una vida extra. Te quedan {self.jugador.vidas}"
            else:
                # Se acabaron todas las vidas globales
                self.jugador.vida = 0
                self.combate_activo = False
                self.derrota = True
                self.log_daño = "¡DERROTA TOTAL! Has reprobado todas tus oportunidades."

    def _obtener_estado_final(self):
        """
        Le dice al ControladorMaestro a donde ir ahora.
        """
        if self.victoria:
            # Ganas XP y revisas si subes de nivel
            subio = self.jugador.ganar_xp(40)
            return "EVOLUCION" if subio else "JUEGO"
        
        if self.derrota:
            # Mandamos el aviso de muerte para que Maestro ponga la pantalla oscura
            return "PANTALLA_MUERTE"
            
        return "JUEGO"