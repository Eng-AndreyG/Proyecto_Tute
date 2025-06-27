from src.backend.carta import Carta
from abc import ABC, abstractmethod


class IAStrategy(ABC): # Define una interfaz para las estrategias de IA
    @abstractmethod
    def jugar_carta(self, mano: list, baza_palo: str) -> "Carta":
        pass

class IAFacil(IAStrategy): # Implementa una estrategia de IA fácil
    def jugar_carta(self, mano: list, baza_palo: str) -> "Carta":
        import random
        return random.choice(mano)

class IAMedio(IAStrategy): # Implementa una estrategia de IA media
    def jugar_carta(self, mano: list, baza_palo: str) -> "Carta":
        cartas_palo = [c for c in mano if c.palo == baza_palo] if baza_palo else []
        return max(cartas_palo, key=lambda c: c.puntos) if cartas_palo else max(mano, key=lambda c: c.puntos)