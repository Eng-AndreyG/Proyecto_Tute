from .estado_base import EstadoJuego

class EstadoFinPartida(EstadoJuego):
    def __init__(self, ganador: str):
        self.ganador = ganador

    def manejar_evento(self, contexto, evento: str):
        contexto.notificar(f"partida_terminada:{self.ganador}")