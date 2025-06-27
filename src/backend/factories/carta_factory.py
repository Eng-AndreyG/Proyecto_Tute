from ..carta import Carta

class CartaFactory:
    @staticmethod
    def crear_carta(palo: str, valor: str) -> Carta:
        puntos = {
            "As": 11, "3": 10, "Rey": 4, # Se asginan puntos a las cartas
            "Caballo": 3, "Sota": 2
        }.get(valor, 0)  # Default: 0 puntos
        
        imagen_path = f"assets/imagenes/{palo}/{valor}.png" # Ruta de la imagen de la carta
        return Carta(palo, valor, puntos, imagen_path)  