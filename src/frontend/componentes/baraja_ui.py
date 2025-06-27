import pygame
from pathlib import Path

class BarajaUI:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.cartas = []
        self._cargar_imagenes()
        
    def _cargar_imagenes(self):
        self.reverso = pygame.image.load("assets/imagenes/back.jpg")
        self.reverso = pygame.transform.scale(self.reverso, (100, 150))
        
    def dibujar(self, pantalla):
        # Dibuja cartas apiladas con efecto 3D
        for i in range(5):
            pantalla.blit(self.reverso, (self.x + i*2, self.y + i*2))
    
    def repartir_animacion(self, carta_ui, objetivo_x, objetivo_y):
        # Lógica para animar el reparto
        carta_ui.objetivo_x = objetivo_x
        carta_ui.objetivo_y = objetivo_y