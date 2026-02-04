import os

# Esta clase organiza y entrega las rutas de todas las imagenes del juego
class GestorRutas:
    def __init__(self):
        # 1. Busca la carpeta 'Imagenes' automaticamente sin importar donde instales el juego
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ruta_imagenes = os.path.join(base_dir, "Imagenes")
        
        # 2. DICCIONARIOS DE FONDOS
        # Aqui asocias el nombre del lugar del mapa con su archivo de imagen
        self.fondos_mapa = {
            "Inicio":  "Fondo_Inicial.png",
            "Campus":  "Fondo_Universidad.png",
            "Comedor": "Fondo_Comedor.png",
            "Ed39":    "Fondo_Ed39.png",
            "Piso 5":  "Banios_P5.png"  
        }

        # Aqui puedes poner fondos distintos para cuando estas peleando en esos mismos lugares
        self.fondos_combate = {
            "Inicio":  "Fondo_Inicial.png",
            "Campus":  "Fondo_Universidad.png",
            "Comedor": "Fondo_Comedor.png",
            "Ed39":    "Fondo_Ed39.png",
            "Piso 5":  "Banios_P5.png" 
        }

    def obtener_ruta_fondo(self, nodo, es_combate=False):
        """
        Busca que imagen corresponde al lugar donde estas parado.
        Si es_combate es True, mira la lista de fondos de pelea.
        """
        if es_combate:
            nombre_archivo = self.fondos_combate.get(nodo, "Fondo_Comedor.png")
        else:
            nombre_archivo = self.fondos_mapa.get(nodo, "Fondo_Inicial.png")
            
        return self._construir_ruta(nombre_archivo)
    
    def obtener_ruta_personaje(self, clase, nombre_evolucion):
        """
        BUSQUEDA INTELIGENTE: Intenta encontrar la imagen del personaje evolucionado.
        Si tu evolucion es 'Maestro del Sol', buscara un archivo que contenga esas palabras.
        """
        # Si no ha evolucionado, devuelve la imagen base (ej. P_Fuego.png)
        if not nombre_evolucion or nombre_evolucion == "Desconocido":
            return self._construir_ruta(f"P_{clase}.png")

        # Limpia el nombre (quita 'el', 'la', 'de') para buscar solo palabras importantes
        conectores = ["el", "la", "los", "las", "un", "una", "de", "del", "en", "y", "o"]
        nombre_limpio = nombre_evolucion.lower().replace("_", " ")
        palabras = nombre_limpio.split()
        palabras_clave = [p for p in palabras if p not in conectores and len(p) > 2]

        try:
            # Escanea la carpeta Imagenes buscando un archivo que coincida con las palabras clave
            if os.path.exists(self.ruta_imagenes):
                todos = os.listdir(self.ruta_imagenes)
                for archivo in todos:
                    if not (archivo.endswith(".png") or archivo.endswith(".jpg")): continue
                    
                    archivo_lower = archivo.lower()
                    # Si el nombre del archivo contiene las palabras de la evolucion, lo elige
                    if all(p in archivo_lower for p in palabras_clave):
                        return self._construir_ruta(archivo)
        except:
            pass
            
        # Si no encuentra nada especial, vuelve a la imagen base
        return self._construir_ruta(f"P_{clase}.png")

    def _construir_ruta(self, nombre_archivo):
        """Une la carpeta de imagenes con el nombre del archivo de forma segura"""
        return os.path.join(self.ruta_imagenes, nombre_archivo)
    
    def obtener_ruta_archivo(self, nombre_archivo):
        """Retorna la ruta de cualquier imagen suelta (iconos, logos, etc)"""
        return self._construir_ruta(nombre_archivo)