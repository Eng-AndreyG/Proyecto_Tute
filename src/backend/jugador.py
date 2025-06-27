from abc import ABC, abstractmethod
from src.backend.carta import Carta

class Jugador(ABC): 
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.mano = []

class JugadorHumano(Jugador): # Representa un jugador humano
    def jugar_carta(self, idx: int) -> "Carta":
        return self.mano.pop(idx)

class JugadorIA(Jugador): # Representa un jugador controlado por IA
    def __init__(self, estrategia: str = "facil"):
        super().__init__("IA")
        self.estrategia = self._cargar_estrategia(estrategia)

    def _cargar_estrategia(self, estrategia: str):
        from .ia import IAFacil, IAMedio
        return IAFacil() if estrategia == "facil" else IAMedio()

    def jugar_carta(self, baza_palo: str) -> "Carta":
        return self.estrategia.jugar_carta(self.mano, baza_palo)