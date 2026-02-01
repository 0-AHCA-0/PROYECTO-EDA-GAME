import pygame


class EvolucionControlador:
    """
    Controlador inteligente para la selección de evolución de habilidades.
    Usa las coordenadas de la vista en lugar de hardcodearlas.
    """
    
    def __init__(self, modelo):
        """
        Inicializa el controlador.
        
        Args:
            modelo: Instancia de GameModel con los datos del jugador.
        """
        self.model = modelo

    def ejecutar(self, eventos, vista):
        """
        Procesa los eventos de selección de habilidad.
        
        Args:
            eventos: Lista de eventos de Pygame.
            vista: Instancia de Estructura_Vista que contiene botones_evolucion.
            
        Returns:
            str: "JUEGO" si se selecciona una habilidad, "EVOLUCION" para continuar.
        """
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Acceder a los botones almacenados en la vista
                for boton_info in vista.botones_evolucion:
                    if boton_info["rect"].collidepoint(evento.pos):
                        # El clic colisionó con este botón
                        return self._seleccionar_habilidad(boton_info, evento.pos)
        
        return "EVOLUCION"
    
    def _seleccionar_habilidad(self, boton_info, pos_clic):
        """
        Asigna la habilidad seleccionada al jugador.
        
        Args:
            boton_info: Diccionario con datos del botón (rect, habilidad, indice).
            pos_clic: Posición del clic del ratón (x, y).
            
        Returns:
            str: "JUEGO" para volver al mapa.
        """
        jugador = self.model.obtener_jugador_actual()
        
        # Obtener la habilidad seleccionada
        habilidad_seleccionada = boton_info["habilidad"]
        
        # Asignar al jugador
        jugador.habilidad_actual = habilidad_seleccionada
        
        print(f"✓ {jugador.nombre} aprendió: {habilidad_seleccionada}")
        
        # Retornar al mapa tras evolucionar
        return "JUEGO"
