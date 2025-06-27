import pygame
from ..componentes import Boton, SelectorDificultad

class MenuPrincipal:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.fuente_titulo = pygame.font.SysFont("Arial", 64, bold=True)
        self.boton_jugar = Boton(412, 350, 200, 60, "JUGAR", (0, 180, 0))
        self.selector = SelectorDificultad(362, 450)
        
    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_jugar.clickeado(pygame.mouse.get_pos()):
                    return {
                        'estado': 'partida',
                        'dificultad': self.selector.dificultad  # Asegúrate que esto devuelve 'fácil', 'medio' o 'difícil'
                    }
                self.selector.manejar_click(pygame.mouse.get_pos())
        return None
    
    def dibujar(self):
        self.pantalla.fill((20, 20, 50))
        
        # Título
        titulo = self.fuente_titulo.render("TUTE", True, (255, 215, 0))
        self.pantalla.blit(titulo, (
            (self.pantalla.get_width() - titulo.get_width()) // 2, 
            150
        ))
        
        # Botón y selector
        self.boton_jugar.dibujar(self.pantalla)
        self.selector.dibujar(self.pantalla)
        
        pygame.display.flip()