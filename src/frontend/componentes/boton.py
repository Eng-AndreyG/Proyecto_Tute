import pygame

class Boton:
    def __init__(self, x: int, y: int, ancho: int, alto: int, texto: str, color: tuple):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color = color
        self.fuente = pygame.font.SysFont("Arial", 24)
        
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect, border_radius=10)
        texto_render = self.fuente.render(self.texto, True, (255, 255, 255))
        pantalla.blit(texto_render, 
                     (self.rect.x + (self.rect.width - texto_render.get_width()) // 2,
                      self.rect.y + (self.rect.height - texto_render.get_height()) // 2))

    def clickeado(self, pos: tuple) -> bool:
        return self.rect.collidepoint(pos)