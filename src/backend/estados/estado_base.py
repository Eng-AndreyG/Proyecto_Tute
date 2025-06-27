from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.backend.juego import Juego  # Solo para type hints

class EstadoJuego(ABC):
    @abstractmethod
    def manejar_evento(self, contexto: 'Juego', evento: str):
        pass