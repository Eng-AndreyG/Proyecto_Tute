import pygame
from .estados.menu_principal import MenuPrincipal
from .estados.partida import Partida
from .estados.fin_partida import FinPartida

class GUI:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("Tute - Jugador vs IA")
        self.reloj = pygame.time.Clock()
        self.estado_actual = MenuPrincipal(self.pantalla)
        self.dificultad_actual = "medio"  # Valor por defecto

    def cambiar_estado(self, nuevo_estado: str, **kwargs):
        """
        Cambia el estado actual de la aplicación
        Args:
            nuevo_estado: Nombre del estado ('menu', 'partida', 'fin')
            kwargs: Argumentos adicionales (dificultad, ganador)
        """
        if nuevo_estado == "menu":
            self.estado_actual = MenuPrincipal(self.pantalla)
        elif nuevo_estado == "partida":
            self.dificultad_actual = kwargs.get('dificultad', 'medio')
            self.estado_actual = Partida(self.pantalla, self.dificultad_actual)
        elif nuevo_estado == "fin":
            ganador = kwargs.get('ganador', 'humano')
            self.estado_actual = FinPartida(self.pantalla, ganador)

    def manejar_transicion(self, resultado):
        """
        Maneja la transición entre estados según el resultado devuelto
        """
        if resultado == "salir":
            return False
        elif isinstance(resultado, dict):
            if "nuevo_estado" in resultado:
                self.cambiar_estado(**resultado)
            elif "estado" in resultado:  # Para compatibilidad
                resultado["nuevo_estado"] = resultado.pop("estado")
                self.cambiar_estado(**resultado)
        return True

    def run(self):
        """
        Bucle principal del juego
        """
        ejecutando = True
        while ejecutando:
            # Manejo de eventos
            resultado = self.estado_actual.manejar_eventos()
            ejecutando = self.manejar_transicion(resultado)

            # Actualización del estado
            if hasattr(self.estado_actual, 'actualizar'):
                self.estado_actual.actualizar()

            # Renderizado
            self.estado_actual.dibujar()
            pygame.display.flip()
            self.reloj.tick(60)

        pygame.quit()

    def manejar_accion_partida(self, accion: dict):
        """
        Maneja acciones específicas durante la partida
        """
        if accion["accion"] == "jugar_carta":
            try:
                resultado = self.estado_actual.juego.jugar_turno_humano(accion["indice"])
                if resultado:  # Si se completó una baza
                    self.estado_actual._manejar_fin_baza(resultado)
            except Exception as e:
                self.estado_actual.mostrar_error(str(e))