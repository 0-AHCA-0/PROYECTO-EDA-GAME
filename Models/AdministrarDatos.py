import csv
import GrafoHabilidades
import ArbolEvolucion
import Player

class AdministrarDatos:
    
    archivo = "datos/proceso.csv"
    def __init__(self, archivo):
        self.archivo = archivo
        
    def _guardar_partida (self, players):
        try:
            with open(self.archivo, mode='w', newline='', encoding='utf-8') as f:
                write = csv.writer(f)
                write.writerow(["ID","Clase", "XP", "Evolucion", "Habilidad"])
                for p in players:
                    write.writerow([p.id, p.clase. p.vidas, p.xp, p.nivel_evolucion, p.habilidad_actual])
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False
    
    def cargar_partida(self):
        # Esta función la usará Erick para retomar el juego
        partida = []
        try:
            with open(self.archivo, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    partida.append(row)
            return partida
        except FileNotFoundError:
            return None
                