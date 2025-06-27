import pygame
from ..componentes import CartaUI, BarajaUI, Boton
from src.backend.juego import Juego
from src.backend.ia import IAFacil, IAMedio, IADificil
from src.backend.reglas import Reglas

class Partida:
    def __init__(self, pantalla, dificultad: str):
        self.pantalla = pantalla
        self.juego = Juego()
        self.juego.jugador_ia.estrategia = self._elegir_estrategia(dificultad)
        self.baraja_ui = BarajaUI(100, 100)
        self.cartas_ui = []
        self.boton_tute = Boton(800, 650, 150, 50, "Cantar Tute", (200, 50, 50))
        self._inicializar_ui()
        
    def _elegir_estrategia(self, dificultad: str):
        return {
            "fácil": IAFacil(),
            "medio": IAMedio(),
            "difícil": IADificil()
        }[dificultad]
    
    def _inicializar_ui(self):
        # Cartas del jugador (inicialmente ocultas)
        for i, carta in enumerate(self.juego.jugador_humano.mano):
            self.cartas_ui.append(CartaUI(carta, 150 + i * 110, 650, visible=False))
    
    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Click en cartas
                for carta_ui in self.cartas_ui:
                    if carta_ui.contiene_punto(event.pos):
                        carta_ui.visible = not carta_ui.visible
                
                # Click en botón Tute
            if self.boton_tute.clickeado(event.pos):
                if Reglas.puede_cantar_tute(self.juego.jugador_humano.mano):
                    return {
                        'estado': 'fin',
                        'ganador': 'humano'
                    }
    
    def dibujar(self):
        self.pantalla.fill((30, 90, 30))  # Fondo verde
        
        # Dibujar baraja
        self.baraja_ui.dibujar(self.pantalla)
        
        # Dibujar cartas
        for carta_ui in self.cartas_ui:
            carta_ui.dibujar(self.pantalla)
        
        # Botón
        self.boton_tute.dibujar(self.pantalla)
        
        pygame.display.flip()