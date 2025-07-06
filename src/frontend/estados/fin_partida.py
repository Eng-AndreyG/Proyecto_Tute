import pygame
from ..componentes.boton import Boton

class FinPartida:
    def __init__(self, pantalla, ganador: str, puntos_humano: int = 0, puntos_ia: int = 0, mensaje: str = None):
        self.pantalla = pantalla
        self.ganador = ganador
        self.puntos_humano = puntos_humano
        self.puntos_ia = puntos_ia
        self.mensaje_personalizado = mensaje
        
        # Debug: verificar que el mensaje se está recibiendo
        print(f"FinPartida - Ganador: {ganador}, Mensaje: {mensaje}")
        
        self.fuente_titulo = pygame.font.SysFont("Arial", 48, bold=True)
        self.fuente_texto = pygame.font.SysFont("Arial", 32)
        self.fuente_puntos = pygame.font.SysFont("Arial", 28, bold=True)
        self.fuente_mensaje = pygame.font.SysFont("Arial", 24)
        
        # Botones
        self.boton_reiniciar = Boton(350, 480, 150, 50, "Reiniciar", (0, 150, 0))
        self.boton_menu = Boton(350, 560, 150, 50, "Menú Principal", (0, 100, 200))
        self.boton_salir = Boton(350, 640, 150, 50, "Salir", (150, 0, 0))

    def manejar_eventos(self) -> str:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.boton_reiniciar.clickeado(pos):
                    return "reiniciar"
                elif self.boton_menu.clickeado(pos):
                    return "menu"
                elif self.boton_salir.clickeado(pos):
                    return "salir"
        return ""

    def dibujar(self):
        # Fondo
        self.pantalla.fill((30, 30, 60))
        
        # Texto de resultado
        if self.mensaje_personalizado:
            # Dividir mensaje en líneas si contiene saltos de línea
            lineas = self.mensaje_personalizado.split('\n')
            y_inicio = 120
            for i, linea in enumerate(lineas):
                if i == 0:  # Primera línea más grande y colorida
                    texto = self.fuente_titulo.render(
                        linea, 
                        True, 
                        (255, 255, 0) if self.ganador == "humano" else (255, 100, 100)
                    )
                else:  # Líneas adicionales más pequeñas
                    texto = self.fuente_mensaje.render(linea, True, (200, 200, 255))
                
                self.pantalla.blit(texto, (
                    (self.pantalla.get_width() - texto.get_width()) // 2, 
                    y_inicio + i * 50
                ))
        else:
            # Mensaje por defecto
            texto_ganador = self.fuente_titulo.render(
                f"¡{self.ganador.upper()} GANA!", 
                True, 
                (255, 255, 0) if self.ganador == "humano" else (255, 100, 100)
            )
            self.pantalla.blit(texto_ganador, (
                (self.pantalla.get_width() - texto_ganador.get_width()) // 2, 
                120
            ))
        
        # Mostrar puntuación final (más abajo para no superponerse)
        texto_puntos_titulo = self.fuente_texto.render("PUNTUACIÓN FINAL", True, (255, 255, 255))
        self.pantalla.blit(texto_puntos_titulo, (
            (self.pantalla.get_width() - texto_puntos_titulo.get_width()) // 2, 
            280
        ))
        
        # Puntos del jugador humano
        color_humano = (0, 255, 0) if self.ganador == "humano" else (255, 255, 255)
        texto_humano = self.fuente_puntos.render(f"Jugador: {self.puntos_humano} puntos", True, color_humano)
        self.pantalla.blit(texto_humano, (
            (self.pantalla.get_width() - texto_humano.get_width()) // 2, 
            330
        ))
        
        # Puntos de la IA
        color_ia = (0, 255, 0) if self.ganador == "ia" else (255, 255, 255)
        texto_ia = self.fuente_puntos.render(f"IA: {self.puntos_ia} puntos", True, color_ia)
        self.pantalla.blit(texto_ia, (
            (self.pantalla.get_width() - texto_ia.get_width()) // 2, 
            370
        ))
        
        # Diferencia de puntos
        diferencia = abs(self.puntos_humano - self.puntos_ia)
        texto_diferencia = self.fuente_texto.render(f"Diferencia: {diferencia} puntos", True, (200, 200, 200))
        self.pantalla.blit(texto_diferencia, (
            (self.pantalla.get_width() - texto_diferencia.get_width()) // 2, 
            410
        ))
        
        # Botones
        self.boton_reiniciar.dibujar(self.pantalla)
        self.boton_menu.dibujar(self.pantalla)
        self.boton_salir.dibujar(self.pantalla)
        
        pygame.display.flip()