import pygame
from .estados.menu_principal import MenuPrincipal
from .estados.partida import Partida
from .estados.fin_partida import FinPartida

class GUI:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("Tute - Jugador vs IA")
        self.estado_actual = MenuPrincipal(self.pantalla)
        self.reloj = pygame.time.Clock()
        
    def cambiar_estado(self, nuevo_estado: str, **kwargs):
        """Cambia el estado actual de la GUI.
        
        Args:
            nuevo_estado: Nombre del estado ('menu', 'partida', 'fin')
            **kwargs: Argumentos adicionales para el estado:
                - 'dificultad' (str): Para estado 'partida'
                - 'ganador' (str): Para estado 'fin'
        """
        if nuevo_estado == "menu":
            self.estado_actual = MenuPrincipal(self.pantalla)
        elif nuevo_estado == "partida":
            dificultad = kwargs.get('dificultad', 'medio')  # Valor por defecto
            self.estado_actual = Partida(self.pantalla, dificultad)
        elif nuevo_estado == "fin":
            ganador = kwargs.get('ganador', 'humano')  # Valor por defecto
            self.estado_actual = FinPartida(self.pantalla, ganador)
    
    def run(self):
        ejecutando = True
        while ejecutando:
            resultado = self.estado_actual.manejar_eventos()
            
            if resultado == "salir":
                ejecutando = False
            elif isinstance(resultado, dict):
                # Extraemos el tipo de estado y los argumentos adicionales
                estado = resultado.pop('estado')
                self.cambiar_estado(estado, **resultado)
            elif resultado in ["menu", "reiniciar"]:
                self.cambiar_estado(resultado)
            
            self.estado_actual.dibujar()
            self.reloj.tick(60)
        
        pygame.quit()