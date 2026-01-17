class GrafoHabilidades:
    def __init__(self):
        self.__class__grafos = {
            "Fuego": {
                "Chispa": ["Bola de Fuego", "Enviste Igneo"],
                "Bola de Fuego": ["Inferno"],
                "Enviste Igneo": ["Explosion Solar"],
                "Explosión Solar": [],
                "Infierno": []
            },
            "Agua": {
            "Burbuja": ["Squirt", "Sana Sana"],
            "Squirt": ["Tsunami"],
            "Sana Sana": ["Sana Colita de Rana"],
            "Tsunami": [],
            "Sana Colita de Rana": []
            },
            "Tierra": {
                "Terron": ["KKCK", "Lodo"],
                "KKCK": ["Churreta"],
                "Lodo": ["Pantano"],
                "Churreta": [],
                "Pantano": []
            },
            "Aire": {
                "Soplido": ["Afixia", "Levitar"],
                "Afixia": ["Chupa Almas"],
                "Levitar": ["Patada Voladora"],
                "Chupa Almas": [],
                "Patada Voladora": []
            }
        }

            