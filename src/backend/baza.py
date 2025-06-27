from typing import Dict
from src.backend.carta import Carta

class Baza:
    def __init__(self):
        self.cartas_jugadas: Dict[str, 'Carta'] = {}  # {"jugador": Carta}
        self.palo_inicial: str = None

    def agregar_carta(self, jugador: str, carta: 'Carta'):
        if not self.palo_inicial:
            self.palo_inicial = carta.palo
        self.cartas_jugadas[jugador] = carta

    def determinar_ganador(self, palo_triunfo: str) -> str:
        cartas_relevantes = {
            jugador: carta for jugador, carta in self.cartas_jugadas.items()
            if carta.palo == self.palo_inicial or carta.palo == palo_triunfo
        }
        if not cartas_relevantes:
            return next(iter(self.cartas_jugadas.keys()))
        
        return max(
            cartas_relevantes.items(),
            key=lambda item: (item[1].palo == palo_triunfo, item[1].puntos)
        )[0]