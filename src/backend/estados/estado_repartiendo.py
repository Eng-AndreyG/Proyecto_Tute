from .estado_base import EstadoJuego

class EstadoRepartiendo(EstadoJuego):
    def manejar_evento(self, contexto, evento: str):
        if evento == "cartas_repartidas":
            from .estado_jugando import EstadoJugando  # Import local para evitar circularidad
            contexto.cambiar_estado(EstadoJugando())