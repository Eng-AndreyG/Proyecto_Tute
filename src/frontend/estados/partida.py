import pygame
from ..componentes import CartaUI, BarajaUI, Boton
from src.backend.juego import Juego
from src.backend.ia import IAFacil, IAMedio, IADificil

class Partida:
    def __init__(self, pantalla, dificultad: str):
        # Configuración inicial
        self.pantalla = pantalla
        self.juego = Juego()
        self.juego.iniciar_partida()
        self.juego.jugador_ia.estrategia = self._elegir_estrategia(dificultad)
        
        # Elementos UI
        self.baraja_ui = BarajaUI(50, 30)  # Posición ajustada: x=50, y=30
        self.boton_tute = Boton(800, 650, 150, 50, "Cantar Tute", (200, 50, 50))
        self.fuente = pygame.font.SysFont("Arial", 24)
        
        # Estado del juego
        self.cartas_ui = []      # Cartas del jugador (visibles)
        self.cartas_ia_ui = []   # Cartas de la IA (reversos)
        self.mensaje_error = ""
        self.tiempo_mensaje = 0
        
        # Inicializar cartas
        self._inicializar_cartas()

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar clic en cartas del jugador
                for i, carta_ui in enumerate(self.cartas_ui):
                    if carta_ui.contiene_punto(event.pos):
                        try:
                            resultado = self.juego.jugar_turno_humano(i)
                            if resultado:  # Si se completó una baza
                                self._actualizar_manos()
                                if len(self.juego.jugador_humano.mano) == 0:
                                    return {"estado": "fin", "ganador": resultado}
                            return None
                        except Exception as e:
                            self.mostrar_error(str(e))
                
                # Verificar clic en botón de Tute
                if self.boton_tute.clickeado(event.pos):
                    try:
                        self.juego.manejar_evento("tute_cantado")
                        return {"estado": "fin", "ganador": "humano"}
                    except Exception as e:
                        self.mostrar_error(str(e))
        
        return None

    # En el método _inicializar_cartas:
    def _inicializar_cartas(self):
        """Posiciona todas las cartas con espacios adecuados"""
        # Cartas IA (arriba)
        for i, carta in enumerate(self.juego.jugador_ia.mano):
            self.cartas_ia_ui.append(
                CartaUI(carta, 100 + i * 110, 50, visible=False)  # Y=50 para IA
            )
        
        # Cartas Jugador (abajo)
        for i, carta in enumerate(self.juego.jugador_humano.mano):
            self.cartas_ui.append(
                CartaUI(carta, 100 + i * 110, 500, visible=True)  # Y=500 para jugador
            )

    def _elegir_estrategia(self, dificultad: str):
        if dificultad == "facil":
            return IAFacil()
        elif dificultad == "medio":
            return IAMedio()
        elif dificultad == "dificil":
            return IADificil()
        return IAMedio()

    def _actualizar_manos(self):
        """Actualiza las cartas mostradas después de jugar una baza"""
        self.cartas_ui = []
        self.cartas_ia_ui = []
        self._inicializar_cartas()

    def mostrar_error(self, mensaje: str):
        self.mensaje_error = mensaje
        self.tiempo_mensaje = pygame.time.get_ticks()

    def actualizar(self):
        # Limpiar mensajes de error después de 2 segundos
        if self.mensaje_error and pygame.time.get_ticks() - self.tiempo_mensaje > 2000:
            self.mensaje_error = ""

    def dibujar(self):
        self.pantalla.fill((30, 90, 30))  # Fondo verde oscuro
        
        # Dibujar elementos
        self.baraja_ui.dibujar(self.pantalla)
        
        # Cartas de la IA (arriba)
        for carta in self.cartas_ia_ui:
            carta.dibujar(self.pantalla)
        
        # Cartas del jugador (abajo)
        for carta in self.cartas_ui:
            carta.dibujar(self.pantalla)
        
        # Botón de Tute
        self.boton_tute.dibujar(self.pantalla)
        
        # Mensaje de error
        if self.mensaje_error:
            texto = self.fuente.render(self.mensaje_error, True, (255, 0, 0))
            self.pantalla.blit(texto, (400, 300))
        
        pygame.display.flip()