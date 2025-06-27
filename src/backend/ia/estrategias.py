from abc import ABC, abstractmethod
from typing import List
from src.backend.carta import Carta

class IAStrategy(ABC):
    @abstractmethod
    def jugar_carta(self, mano: List[Carta], baza_palo: str) -> Carta:
        pass

class IAFacil(IAStrategy):
    def jugar_carta(self, mano: List[Carta], baza_palo: str) -> Carta:
        import random
        return random.choice(mano)

class IAMedio(IAStrategy):
    def jugar_carta(self, mano: List[Carta], baza_palo: str) -> Carta:
        cartas_palo = [c for c in mano if c.palo == baza_palo] if baza_palo else []
        return max(cartas_palo, key=lambda c: c.puntos) if cartas_palo else max(mano, key=lambda c: c.puntos)

class IADificil(IAStrategy):
    def jugar_carta(self, mano: List[Carta], baza_palo: str) -> Carta:
        # Estrategia avanzada: prioriza triunfos y cartas altas, con memoria de cartas jugadas
        cartas_palo = [c for c in mano if c.palo == baza_palo] if baza_palo else []
        if cartas_palo:
            return max(cartas_palo, key=lambda c: c.puntos)
        else:
            # Si no tiene palo, juega la carta más baja para guardar las buenas
            return min(mano, key=lambda c: c.puntos)