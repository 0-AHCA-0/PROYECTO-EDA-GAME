import sys
from Controllers.ControladorMaestro import ControladorMaestro

def main():
    # Iniciamos el controlador que orquesta todo el MVC
    juego = ControladorMaestro()
    juego.ejecutar()

if __name__ == "__main__":
    main()