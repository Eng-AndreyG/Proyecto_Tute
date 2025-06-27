from .estados.estado_repartiendo import EstadoRepartiendo
from .estados.estado_jugando import EstadoJugando
from .estados.estado_fin import EstadoFinPartida
from .baraja import Baraja
from .jugador import JugadorHumano, JugadorIA
from .baza import Baza
from .reglas import Reglas

class Juego:
    _instance = None

    def __new__(cls): # Patrón Singleton
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.inicializar()
        return cls._instance

    def inicializar(self): # Inicializa el juego 
        self.baraja = Baraja()
        self.jugador_humano = JugadorHumano("Humano")
        self.jugador_ia = JugadorIA("IA")
        self.palo_triunfo = None
        self.baza_actual = Baza()
        self._observers = []
        self._estado = EstadoRepartiendo()  # Estado inicial

    def cambiar_estado(self, nuevo_estado): # Cambia el estado del juego
        self._estado = nuevo_estado
        self.notificar(f"estado_cambiado:{nuevo_estado.__class__.__name__}")

    def manejar_evento(self, evento: str): # Maneja eventos del juego
        self._estado.manejar_evento(self, evento)

    def add_observer(self, observer): # Añade un observador al juego
        self._observers.append(observer)

    def notificar(self, evento: str): # Notifica a todos los observadores
        for obs in self._observers:
            obs.actualizar(evento)

    def iniciar_partida(self): # Inicia una nueva partida
        self.baraja.barajar()
        self.jugador_humano.mano = self.baraja.repartir(8)
        self.jugador_ia.mano = self.baraja.repartir(8)
        self.palo_triunfo = self.baraja.cartas.pop().palo
        self.manejar_evento("cartas_repartidas")  # Cambia a EstadoJugando
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

    def _verificar_fin_partida(self) -> bool: # Verifica si la partida ha terminado
        return len(self.jugador_humano.mano) == 0
    
    @property
    def estado_actual(self) -> str:
        """Devuelve el nombre del estado actual (para debug o GUI)."""
        return self._estado.__class__.__name__