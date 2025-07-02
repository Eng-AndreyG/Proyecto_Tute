from src.backend.baza import Baza
from .estados.estado_repartiendo import EstadoRepartiendo
from .estados.estado_jugando import EstadoJugando
from .estados.estado_fin import EstadoFinPartida
from .baraja import Baraja
from .jugador import JugadorHumano, JugadorIA
from .baza import Baza
from .reglas import Reglas

class Juego:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.inicializar()
        return cls._instance

    def inicializar(self):
        self.baraja = Baraja()
        self.jugador_humano = JugadorHumano("Humano")
        self.jugador_ia = JugadorIA("medio")
        self.palo_triunfo = None
        self.baza_actual = Baza()
        self._observers = []  # Inicializar la lista de observadores

    def __init__(self):
        self._observers = []  # Asegurar que existe
        self.inicializar()

    def add_observer(self, observer):
        """Añade un observador que debe tener método actualizar(evento)."""
        self._observers.append(observer)

    def notificar(self, evento: str):
        """Notifica a todos los observadores."""
        for obs in self._observers:
            try:
                obs.actualizar(evento)
            except Exception as e:
                print(f"Error notificando a observador: {e}")

    def iniciar_partida(self):
        # Inicialización básica
        self.baraja.inicializar()
        self.baraja.barajar()
        self.jugador_humano.mano = self.baraja.repartir(8)
        self.jugador_ia.mano = self.baraja.repartir(8)

        # Establecer triunfo
        self.palo_triunfo = self.baraja.cartas[-1].palo if self.baraja.cartas else "Oros"
        if hasattr(self.jugador_ia.estrategia, 'actualizar_triunfo'):
            self.jugador_ia.estrategia.actualizar_triunfo(self.palo_triunfo)

        # Inicializar baza
        self.baza_actual = Baza()
        self.baza_actual.palo_triunfo = self.palo_triunfo

        # Notificar
        self.notificar("partida_iniciada")

    def jugar_turno_humano(self, carta_idx: int) -> str: # Juega un turno del jugador humano
        if not isinstance(self._estado, EstadoJugando):
            raise RuntimeError("No es el momento de jugar cartas")
        
        carta = self.jugador_humano.jugar_carta(carta_idx)
        self.baza_actual.agregar_carta("humano", carta)
        return self._verificar_baza_completa()

    def jugar_turno_ia(self) -> str: # Juega un turno del jugador IA
        if not isinstance(self._estado, EstadoJugando):
            raise RuntimeError("No es el momento de jugar cartas")
        
        carta = self.jugador_ia.jugar_carta(self.baza_actual.palo_inicial)
        self.baza_actual.agregar_carta("ia", carta)
        return self._verificar_baza_completa()

    def _verificar_baza_completa(self) -> str: # Verifica si la baza está completa
        if len(self.baza_actual.cartas_jugadas) == 2:
            ganador = self.baza_actual.determinar_ganador(self.palo_triunfo)
            self.notificar(f"baza_ganada:{ganador}")
            self.baza_actual = Baza()
            
            if self._verificar_fin_partida():
                self.manejar_evento("partida_terminada")
            return ganador
        return None

    def _verificar_fin_partida(self) -> bool:
        """Verifica si la partida debe terminar (sin cartas en mano y no hay más para repartir)"""
        return (len(self.jugador_humano.mano) == 0 and 
                len(self.jugador_ia.mano) == 0 and
                len(self.baraja.cartas) == 0)
    
    @property
    def estado_actual(self) -> str:
        """Devuelve el nombre del estado actual (para debug o GUI)."""
        return self._estado.__class__.__name__