from .factories import CartaFactory

class Baraja:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.inicializar()
        return cls._instance

    def inicializar(self):
        self.cartas = self._crear_baraja()

    def _crear_baraja(self) -> list:
        factory = CartaFactory()
        palos = ["Oros", "Copas", "Espadas", "Bastos"]
        valores = ["As", "3", "Rey", "Caballo", "Sota", "2", "4", "5", "6", "7"]
        return [factory.crear_carta(palo, valor) for palo in palos for valor in valores]

    def barajar(self):
        import random
        random.shuffle(self.cartas)

    def repartir(self, num_cartas: int) -> list:
        return [self.cartas.pop() for _ in range(num_cartas)]