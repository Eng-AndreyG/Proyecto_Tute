# Este archivo es el punto de entrada del juego de Tute.
# Aquí se inicializa el juego y se manejan los eventos principales.
# Esta pensado para hacer pruebas rápidas y ver el flujo del juego.
from src.backend.juego import Juego

juego = Juego()
juego.iniciar_partida()

# Verificar estado actual
print("Juego iniciado. Estado actual:", juego.estado_actual)  # Debe ser "EstadoJugando"

# Simular evento
juego.manejar_evento("tute_cantado")
print("Estado después de cantar Tute:", juego.estado_actual)  # Debe ser "EstadoFinPartida"