import pygame

class SelectorDificultad:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.opciones = ["Fácil", "Medio", "Difícil"]
        self.seleccionado = 1  # Medio por defecto
        self.fuente = pygame.font.SysFont("Arial", 28)
        self.ancho_boton = 100
        self.alto_boton = 40
        
    @property
    def dificultad(self):
        return self.opciones[self.seleccionado].lower()
    
    def manejar_click(self, pos: tuple):
        for i in range(len(self.opciones)):
            rect = pygame.Rect(
                self.x + i * (self.ancho_boton + 10),
                self.y,
                self.ancho_boton,
                self.alto_boton
            )
            if rect.collidepoint(pos):
                self.seleccionado = i
                return True
        return False
    
    def dibujar(self, pantalla):
        for i, opcion in enumerate(self.opciones):
            color = (100, 200, 100) if i == self.seleccionado else (70, 70, 70)
            pygame.draw.rect(
                pantalla, color,
                (self.x + i * (self.ancho_boton + 10), self.y, self.ancho_boton, self.alto_boton),
                border_radius=5
            )
            texto = self.fuente.render(opcion, True, (255, 255, 255))
            pantalla.blit(
                texto,
                (self.x + i * (self.ancho_boton + 10) + (self.ancho_boton - texto.get_width()) // 2,
                 self.y + (self.alto_boton - texto.get_height()) // 2)
            )