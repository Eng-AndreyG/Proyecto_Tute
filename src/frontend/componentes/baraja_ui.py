import pygame
import os

class BarajaUI:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y + 250  
        self.reverso = self._cargar_imagen()
        
    def _cargar_imagen(self):
        try:
            ruta = os.path.join("assets", "imagenes", "back.jpg")
            imagen = pygame.image.load(ruta)
            return pygame.transform.scale(imagen, (100, 150))
        except Exception as e:
            print(f"Error cargando reverso: {str(e)}")
            superficie = pygame.Surface((100, 150))
            superficie.fill((30, 30, 120))  # Azul oscuro
            return superficie
    
    def dibujar(self, pantalla):
        # Dibujar 3 cartas apiladas
        for i in range(3):
            pantalla.blit(self.reverso, (self.x + i*2, self.y + i*2))