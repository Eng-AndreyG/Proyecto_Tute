from typing import List, Optional
from src.backend.carta import Carta

class IAStrategy:
    """Clase base abstracta para todas las estrategias de IA."""
    def __init__(self):
        self.triunfo = None  # Palo de triunfo (se actualiza al iniciar la partida)

    def jugar_carta(self, mano: List[Carta], palo_inicial: Optional[str] = None) -> Carta:
        """
        Selecciona una carta para jugar según la estrategia.
        
        Args:
            mano: Lista de cartas disponibles.
            palo_inicial: Palo de la primera carta jugada en la baza (None si es la primera).
        
        Returns:
            Carta seleccionada.
        """
        raise NotImplementedError("Método abstracto")

    def actualizar_triunfo(self, triunfo: str):
        """Actualiza el palo de triunfo (debe llamarse al inicio de cada partida)."""
        self.triunfo = triunfo

    def _filtrar_por_palo(self, cartas: List[Carta], palo: str) -> List[Carta]:
        """Filtra cartas por palo."""
        return [c for c in cartas if c.palo == palo]

    def _mejor_carta(self, cartas: List[Carta]) -> Carta:
        """Devuelve la carta con más puntos del conjunto."""
        return max(cartas, key=lambda c: c.puntos)

    def _peor_carta(self, cartas: List[Carta]) -> Carta:
        """Devuelve la carta con menos puntos del conjunto."""
        return min(cartas, key=lambda c: c.puntos)


class IAFacil(IAStrategy):
    """IA fácil: Juega cartas aleatorias sin estrategia."""
    def jugar_carta(self, mano: List[Carta], palo_inicial: Optional[str] = None) -> Carta:
        import random
        return random.choice(mano)


class IAMedio(IAStrategy):
    """IA intermedia: Sigue el palo inicial y prioriza cartas altas."""
    def jugar_carta(self, mano: List[Carta], palo_inicial: Optional[str] = None) -> Carta:
        # 1. Si hay palo inicial, seguirlo
        if palo_inicial:
            cartas_palo = self._filtrar_por_palo(mano, palo_inicial)
            if cartas_palo:
                return self._mejor_carta(cartas_palo)
        
        # 2. Si no, jugar la peor carta (conservar buenas cartas)
        return self._peor_carta(mano)


class IADificil(IAMedio):
    """IA difícil: Estrategia avanzada con manejo de triunfos."""
    def jugar_carta(self, mano: List[Carta], palo_inicial: Optional[str] = None) -> Carta:
        # 1. Seguir palo inicial si es posible
        if palo_inicial:
            cartas_palo = self._filtrar_por_palo(mano, palo_inicial)
            if cartas_palo:
                return self._mejor_carta(cartas_palo)
        
        # 2. Jugar triunfo más bajo si no se puede seguir el palo
        if self.triunfo:
            cartas_triunfo = self._filtrar_por_palo(mano, self.triunfo)
            if cartas_triunfo:
                return self._peor_carta(cartas_triunfo)
        
        # 3. Jugar la peor carta disponible
        return self._peor_carta(mano)