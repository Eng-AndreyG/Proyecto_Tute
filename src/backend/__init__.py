# Exporta clases del backend
from .juego import Juego
from .carta import Carta
from .baraja import Baraja
from .jugador import JugadorHumano, JugadorIA
from .baza import Baza
from .reglas import Reglas
from .factories import CartaFactory
from .ia import IAFacil, IAMedio, IADificil

__all__ = [
    'Juego',
    'Carta',
    'Baraja',
    'JugadorHumano',
    'JugadorIA',
    'Baza',
    'Reglas',
    'CartaFactory',
    'IAFacil',
    'IAMedio',
    'IADificil'
]