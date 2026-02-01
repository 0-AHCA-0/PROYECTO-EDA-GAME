#Clase jugador donde se especificaran los atributos de cada entidad
class Entidad:
    def __init__(self, nombre, vida, dano):
        self.nombre = nombre
        self.vida = vida
        self.dano = dano
        

class Player(Entidad):
    
    #inicializamos los valores del jugagor y donde se va a encontrar
    def __init__(self, id_player, clase):
        super().__init__(f"Jugador{id_player}", vida=100, dano=100)
        self.id = id_player
        self.clase = clase
        self.vidas = 5
        self.xp = 0
        self.nivel_evolucion = 1
        self.habilidad_actual = self.obtener_habilidad_inicial()
        self.vivo = True
        self.nodo_actual = "Inicio"
    
    #Funcion para obtener la habilidad inicial
    def obtener_habilidad_inicial(self):
        iniciales = {"Fuego": "Chispa", "Agua": "Burbuja", "Tierra": "Terron", "Aire": "Soplido"}
        return iniciales.get(self.clase, "Desconocido")
    
    #Funcion para saber cuando debe subir de nivel el jugador.
    def ganar_xp(self, cantidad):
        self.xp += cantidad
        subio = False
        
        # Si llega a 100 o más, sube nivel y podemos resetear o restar los 100
        if self.xp >= 100 and self.nivel_evolucion < 3:
            self.nivel_evolucion += 1
            self.xp = 0  # Reiniciamos para que la barra vuelva a empezar
            subio = True
            print(f"¡{self.nombre} ha evolucionado al Nivel {self.nivel_evolucion}!")
        
        return subio
    
class Enemy(Entidad):
    def __init__(self, nombre, dificultad):
        super().__init__(
            nombre,
            vida=50 * dificultad,
            dano=5 * dificultad
        )
        self.dificultad = dificultad