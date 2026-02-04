import sys
from Controllers.ControladorMaestro import ControladorMaestro

def main():
    juego = ControladorMaestro()
    juego.ejecutar()

if __name__ == "__main__":
    main()