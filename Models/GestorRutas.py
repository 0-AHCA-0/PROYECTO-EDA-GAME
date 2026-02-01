import os

class GestorRutas:
    def __init__(self):
        # 1. Calculamos la ruta base de las imágenes UNA VEZ
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ruta_imagenes = os.path.join(base_dir, "Imagenes")
        
        # 2. DICCIONARIOS DE FONDOS
        
        #Aqui se agrega las imagenes de fondo del mapa
        self.fondos_mapa = {
            "Inicio":  "Fondo_Inicial.png",
            "Campus":  "Fondo_Universidad.png",
            "Comedor": "Fondo_Comedor.png",
            "Ed39":    "Fondo_Ed39.png",
            "Piso 5":  "Fondo_Piso5.png"  
        }

        #Aqui se agregan las imagenes de fondo de combate
        self.fondos_combate = {
            "Inicio":  "Fondo_Inicial.png",
            "Campus":  "Fondo_Universidad.png",
            "Comedor": "Fondo_Comedor.png",
            "Ed39":    "Fondo_Ed39.png",
            "Piso 5":  "Fondo_Boss_Final.png" 
        }

    #funcion para obtener la ruta del fondo
    def obtener_ruta_fondo(self, nodo, es_combate=False):
        """
        Retorna la ruta del fondo.
        Si es_combate=True, busca en el diccionario de combate (para el Boss).
        """
        if es_combate:
            nombre_archivo = self.fondos_combate.get(nodo, "Fondo_Comedor.png")
        else:
            nombre_archivo = self.fondos_mapa.get(nodo, "Fondo_Inicial.png")
            
        return self._construir_ruta(nombre_archivo)
    

    #Funcion para obtener la ruta del personaje
    def obtener_ruta_personaje(self, clase, nombre_evolucion):
        """
        BÚSQUEDA INTELIGENTE DE IMAGEN (Centralizada aquí)
        """
        # Si no hay nombre, devolvemos la base
        if not nombre_evolucion or nombre_evolucion == "Desconocido":
            return self._construir_ruta(f"P_{clase}.png")

        # Lógica de limpieza
        conectores = ["el", "la", "los", "las", "un", "una", "de", "del", "en", "y", "o"]
        nombre_limpio = nombre_evolucion.lower().replace("_", " ")
        palabras = nombre_limpio.split()
        palabras_clave = [p for p in palabras if p not in conectores and len(p) > 2]

        try:
            if os.path.exists(self.ruta_imagenes):
                todos = os.listdir(self.ruta_imagenes)
                for archivo in todos:
                    if not (archivo.endswith(".png") or archivo.endswith(".jpg")): continue
                    
                    # Verificamos palabras clave
                    archivo_lower = archivo.lower()
                    if all(p in archivo_lower for p in palabras_clave):
                        return self._construir_ruta(archivo)
        except:
            pass
            
        # Fallback
        return self._construir_ruta(f"P_{clase}.png")

    def _construir_ruta(self, nombre_archivo):
        """Método privado para unir la ruta base con el archivo"""
        ruta = os.path.join(self.ruta_imagenes, nombre_archivo)
        # Si el archivo no existe, devuelve una ruta segura
        if not os.path.exists(ruta):
            pass 
        return ruta
    
    
    def obtener_ruta_archivo(self, nombre_archivo):
        """
        Retorna la ruta directa de CUALQUIER imagen sin buscar en los diccionarios de mapas.
        Útil para el Menú, Iconos, etc.
        """
        return self._construir_ruta(nombre_archivo)