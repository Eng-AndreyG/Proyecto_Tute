from .estado_base import EstadoJuego

class EstadoJugando(EstadoJuego):
    def manejar_evento(self, contexto, evento: str):
        if evento == "tute_cantado":
            from .estado_fin import EstadoFinPartida  # Import local
            contexto.cambiar_estado(EstadoFinPartida(ganador="humano"))
        elif evento == "partida_terminada":
            from .estado_fin import EstadoFinPartida  # Import local
            contexto.cambiar_estado(EstadoFinPartida(ganador="ia"))