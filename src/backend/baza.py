from src.backend.carta import Carta

class Baza:
    def __init__(self):
        self.cartas_jugadas = []  # Lista de tuplas (jugador, carta)
        self.palo_inicial = None
        self.palo_triunfo = None  # Nuevo atributo

    def agregar_carta(self, jugador: str, carta: 'Carta'):
        if not self.palo_inicial and jugador == "humano":  # Solo humano establece palo inicial
            self.palo_inicial = carta.palo
        self.cartas_jugadas.append((jugador, carta))

    def determinar_ganador(self) -> str:  # Eliminamos palo_triunfo como parámetro
        if len(self.cartas_jugadas) != 2:
            return "humano"  # Por defecto si hay error
            
        carta_humano = self.cartas_jugadas[0][1]
        carta_ia = self.cartas_jugadas[1][1]

        # Si la IA jugó triunfo y humano no
        if carta_ia.palo == self.palo_triunfo and carta_humano.palo != self.palo_triunfo:
            return "ia"
        
        # Si humano jugó triunfo y IA no
        if carta_humano.palo == self.palo_triunfo and carta_ia.palo != self.palo_triunfo:
            return "humano"
        
        # Si ambos jugaron el mismo palo (inicial o triunfo)
        if carta_ia.palo == carta_humano.palo:
            return "ia" if carta_ia.puntos > carta_humano.puntos else "humano"
        
        # Si jugaron palos diferentes y ninguno es triunfo
        return "ia" if carta_ia.palo == self.palo_inicial else "humano"