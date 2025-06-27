from src.backend.carta import Carta
from typing import List

class Reglas:
    @staticmethod
    def validar_jugada(mano: List['Carta'], carta_jugada: 'Carta', palo_inicial: str) -> bool:
        tiene_palo = any(c.palo == palo_inicial for c in mano)
        return not tiene_palo or carta_jugada.palo == palo_inicial

    @staticmethod
    def calcular_puntos(cartas: List['Carta']) -> int:
        return sum(c.puntos for c in cartas)

    @staticmethod
    def puede_cantar_tute(mano: List['Carta']) -> bool:
        reyes = sum(1 for c in mano if c.valor == "Rey")
        caballos = sum(1 for c in mano if c.valor == "Caballo")
        return reyes == 4 or caballos == 4