from src.backend.carta import Carta
from src.backend.factories import CartaFactory

class Baraja:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.inicializar()
        return cls._instance

    def inicializar(self):
        """Inicializa con exactamente 40 cartas (sin 8s y 9s)"""
        self.cartas = self._crear_baraja_valida()
        self.barajar()

    def _crear_baraja_valida(self) -> list:
        factory = CartaFactory()
        palos = ["Oros", "Copas", "Espadas", "Bastos"]
        valores = ["As", "2", "3", "4", "5", "6", "7", "Sota", "Caballo", "Rey"]  # Sin 8 ni 9
        return [factory.crear_carta(palo, valor) for palo in palos for valor in valores]

    def barajar(self):
        import random
        random.shuffle(self.cartas)

    def repartir(self, num_cartas: int) -> list:
        """Reparte exactamente el número de cartas solicitado o menos si no hay suficientes"""
        num_a_repartir = min(num_cartas, len(self.cartas))
        return [self.cartas.pop() for _ in range(num_a_repartir)] if num_a_repartir > 0 else []