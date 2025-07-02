from typing import List, Optional
from src.backend.carta import Carta

class IAStrategy:
    """Clase base abstracta para todas las estrategias de IA."""
    def __init__(self):
        self.triunfo = None  # Palo de triunfo
        self.cartas_vistas = set()  # Para tracking de cartas

    def jugar_carta(self, mano: List[Carta], palo_inicial: Optional[str] = None) -> Carta:
        raise NotImplementedError("Método abstracto")

    def actualizar_triunfo(self, triunfo: str):
        self.triunfo = triunfo

    def registrar_carta(self, carta: Carta):
        """Registra una carta como vista/jugada"""
        self.cartas_vistas.add((carta.palo, carta.valor))

    def _filtrar_por_palo(self, cartas: List[Carta], palo: str) -> List[Carta]:
        return [c for c in cartas if c.palo == palo]

    def _mejor_carta(self, cartas: List[Carta]) -> Carta:
        return max(cartas, key=lambda c: c.puntos)

    def _peor_carta(self, cartas: List[Carta]) -> Carta:
        return min(cartas, key=lambda c: c.puntos)

    def _carta_valida(self, carta: Carta) -> bool:
        """Verifica si la carta no ha sido jugada antes"""
        return (carta.palo, carta.valor) not in self.cartas_vistas

class IAFacil(IAStrategy):
    def jugar_carta(self, mano: List[Carta], palo_inicial: Optional[str] = None) -> Carta:
        # Filtrar cartas no jugadas
        cartas_validas = [c for c in mano if self._carta_valida(c)] or mano
        
        if palo_inicial:
            cartas_palo = self._filtrar_por_palo(cartas_validas, palo_inicial)
            if cartas_palo:
                return cartas_palo[0]  # Juega la primera
        
        return self._peor_carta(cartas_validas)

class IAMedio(IAStrategy):
    def jugar_carta(self, mano: List[Carta], palo_inicial: Optional[str] = None) -> Carta:
        # Filtrar cartas no jugadas
        cartas_validas = [c for c in mano if self._carta_valida(c)] or mano
        
        if palo_inicial:
            cartas_palo = self._filtrar_por_palo(cartas_validas, palo_inicial)
            if cartas_palo:
                return self._mejor_carta(cartas_palo)
        
        if self.triunfo:
            triunfos = self._filtrar_por_palo(cartas_validas, self.triunfo)
            if triunfos:
                return self._peor_carta(triunfos)
        
        return self._peor_carta(cartas_validas)

class IADificil(IAMedio):
    def __init__(self):
        super().__init__()
        self.cartas_restantes = []  # Para conteo avanzado

    def actualizar_triunfo(self, triunfo: str):
        super().actualizar_triunfo(triunfo)
        # Inicializar tracking de cartas
        self._inicializar_cartas_restantes()

    def _inicializar_cartas_restantes(self):
        from src.backend.factories import CartaFactory
        factory = CartaFactory()
        palos = ["Oros", "Copas", "Espadas", "Bastos"]
        valores = ["As", "2", "3", "4", "5", "6", "7", "Sota", "Caballo", "Rey"]
        self.cartas_restantes = [factory.crear_carta(palo, valor) for palo in palos for valor in valores]

    def jugar_carta(self, mano: List[Carta], palo_inicial: Optional[str] = None) -> Carta:
        # Actualizar cartas restantes
        self.cartas_restantes = [c for c in self.cartas_restantes 
                               if (c.palo, c.valor) not in self.cartas_vistas]
        
        # Filtrar cartas no jugadas
        cartas_validas = [c for c in mano if self._carta_valida(c)] or mano
        
        # Lógica avanzada de decisión
        if palo_inicial:
            cartas_palo = self._filtrar_por_palo(cartas_validas, palo_inicial)
            if cartas_palo:
                # Calcular probabilidades
                cartas_palo_restantes = [c for c in self.cartas_restantes 
                                       if c.palo == palo_inicial]
                if cartas_palo_restantes:
                    return self._mejor_carta(cartas_palo)
                return self._peor_carta(cartas_palo)
        
        if self.triunfo:
            triunfos = self._filtrar_por_palo(cartas_validas, self.triunfo)
            if triunfos:
                return self._peor_carta(triunfos)
        
        return self._peor_carta(cartas_validas)