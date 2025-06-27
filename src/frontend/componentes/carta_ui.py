import pygame

class CartaUI:
    def __init__(self, carta_backend, x: int, y: int):
        self.carta = carta_backend
        self.x = x
        self.y = y
        self.ancho = 100
        self.alto = 150
        self.seleccionada = False
        self.objetivo_x = x  # Para animación
        self.objetivo_y = y
        self._cargar_imagen()

    def _cargar_imagen(self):
        try:
            palo = self.carta.palo.upper()
            valor = self.carta.valor
            ruta = f"assets/imagenes/{palo}/{valor}.jpg"
            self.imagen = pygame.image.load(ruta)
            self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
        except:
            ruta = "assets/imagenes/back.jpg"
            self.imagen = pygame.image.load(ruta)
            self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))

    def actualizar_posicion(self):
        # Suaviza el movimiento hacia el objetivo
        self.x += (self.objetivo_x - self.x) * 0.2
        self.y += (self.objetivo_y - self.y) * 0.2

    def dibujar(self, pantalla):
        self.actualizar_posicion()
        pantalla.blit(self.imagen, (self.x, self.y))
        if self.seleccionada:
            pygame.draw.rect(pantalla, (255, 255, 0), (self.x, self.y, self.ancho, self.alto), 3)

    def contiene_punto(self, pos: tuple) -> bool:
        return (self.x <= pos[0] <= self.x + self.ancho and 
                self.y <= pos[1] <= self.y + self.alto)