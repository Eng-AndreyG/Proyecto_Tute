import pygame
from ..componentes.boton import Boton

class FinPartida:
    def __init__(self, pantalla, ganador: str):
        self.pantalla = pantalla
        self.ganador = ganador
        self.fuente_titulo = pygame.font.SysFont("Arial", 48, bold=True)
        self.fuente_texto = pygame.font.SysFont("Arial", 32)
        
        # Botones
        self.boton_reiniciar = Boton(350, 400, 150, 50, "Reiniciar", (0, 150, 0))
        self.boton_menu = Boton(350, 480, 150, 50, "Menú Principal", (0, 100, 200))
        self.boton_salir = Boton(350, 560, 150, 50, "Salir", (150, 0, 0))

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
        texto_ganador = self.fuente_titulo.render(
            f"¡{self.ganador.upper()} GANA!", 
            True, 
            (255, 255, 0) if self.ganador == "humano" else (255, 100, 100)
        )
        self.pantalla.blit(texto_ganador, (
            (self.pantalla.get_width() - texto_ganador.get_width()) // 2, 
            200
        ))
        
        # Botones
        self.boton_reiniciar.dibujar(self.pantalla)
        self.boton_menu.dibujar(self.pantalla)
        self.boton_salir.dibujar(self.pantalla)
        
        pygame.display.flip()