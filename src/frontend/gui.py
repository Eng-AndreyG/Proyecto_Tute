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
            puntos_humano = kwargs.get('puntos_humano', 0)
            puntos_ia = kwargs.get('puntos_ia', 0)
            mensaje = kwargs.get('mensaje', None)
            self.estado_actual = FinPartida(self.pantalla, ganador, puntos_humano, puntos_ia, mensaje)

    def manejar_transicion(self, resultado):
        if resultado == "salir":
            return False
        
        # Manejar reinicio especial para limpiar el singleton
        if resultado == "reiniciar":
            # Forzar nueva instancia del juego limpiando los singletons
            from src.backend.juego import Juego
            from src.backend.baraja import Baraja
            Juego._instance = None
            Baraja._instance = None
            self.cambiar_estado("partida", dificultad=self.dificultad_actual)
            return True
        
        # Manejar ir al menú principal
        if resultado == "menu":
            # Limpiar los singletons también cuando se va al menú
            from src.backend.juego import Juego
            from src.backend.baraja import Baraja
            Juego._instance = None
            Baraja._instance = None
            self.cambiar_estado("menu")
            return True
        
        if isinstance(resultado, dict):
            try:
                if "nuevo_estado" in resultado:
                    self.cambiar_estado(**resultado)
                elif "estado" in resultado:  # Para compatibilidad
                    resultado["nuevo_estado"] = resultado.pop("estado")
                    self.cambiar_estado(**resultado)
            except Exception as e:
                print(f"Error en transición: {e}")
                return False
        
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