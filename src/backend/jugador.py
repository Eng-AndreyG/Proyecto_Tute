from src.backend.carta import Carta
from src.backend.ia.estrategias import IAFacil, IAMedio, IADificil
from typing import List

class Jugador:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.mano = []

class JugadorHumano(Jugador):
    def jugar_carta(self, idx: int) -> Carta:
        return self.mano.pop(idx)

class JugadorIA(Jugador):
    def __init__(self, estrategia: str = "facil"):
        super().__init__("IA")
        self.estrategia = self._cargar_estrategia(estrategia)
        
    def recibir_mano(self, mano: List[Carta]):
        self.mano = mano
        if isinstance(self.estrategia, IADificil):
            self.estrategia.registrar_mano_inicial(mano)

    def _cargar_estrategia(self, estrategia: str):
        estrategias = {
            "facil": IAFacil(),
            "medio": IAMedio(),
            "dificil": IADificil()
        }
        return estrategias.get(estrategia.lower(), IAMedio())
    
    def jugar_carta(self, palo_inicial: str = None) -> Carta:
        return self.estrategia.jugar_carta(self.mano, palo_inicial)