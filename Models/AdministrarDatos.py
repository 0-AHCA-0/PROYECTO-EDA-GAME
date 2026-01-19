import csv
import os
#Clase para inicializar los atributos de la carta (personaje) y jugardarlos en un csv, para luego cargarlo.
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
    
    #Funcion para retomar el juego (Se [uede usar para retomar la partida)
    def cargar_partida(self):
        partida = []
        try:
            with open(self.archivo, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    partida.append(row)
            return partida
        except FileNotFoundError:
            return None
    
    # Guarda el proceso de los jugadores, si no hay captura la excepcion
    def leer_csv_completo(self):
        try:
            with open(self.archivo, mode='r', encoding='utf-8') as f:
                datos = list(csv.DictReader(f))
                return datos if datos else None
        except FileNotFoundError:
            return None
                