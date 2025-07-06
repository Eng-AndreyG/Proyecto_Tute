import pygame
import os

class CartaUI:
    def __init__(self, carta_backend, x: int, y: int, visible: bool = True):
        self.carta = carta_backend
        self.x = x
        self.y = y
        self.ancho = 100
        self.alto = 150
        self.visible = visible
        self.seleccionada = False
        self.rotacion = 0  # Ángulo de rotación en grados
        self.imagen = self._cargar_imagen()

    def _mapear_valor_archivo(self, valor: str) -> str:
        """Convierte nombres de cartas a números para archivos"""
        mapeo = {
            'As': '1',
            '3': '3',
            'Rey': '12',
            'Caballo': '11',
            'Sota': '10',
            '2': '2',
            '4': '4',
            '5': '5',
            '6': '6',
            '7': '7'
        }
        return mapeo.get(valor, valor)

    def _cargar_imagen(self):
        try:
            # Mapeo de palos a nombres de carpeta
            mapeo_palos = {
                'Espadas': 'ESPADA',
                'Bastos': 'BASTO',
                'Copas': 'COPA',
                'Oros': 'ORO'
            }
            
            palo_carpeta = mapeo_palos.get(self.carta.palo, self.carta.palo)
            valor_archivo = self._mapear_valor_archivo(self.carta.valor)
            
            if self.visible:
                ruta = os.path.join("assets", "imagenes", palo_carpeta, f"{valor_archivo}.jpg")
                imagen = pygame.image.load(ruta)
            else:
                ruta = os.path.join("assets", "imagenes", "back.jpg")
                imagen = pygame.image.load(ruta)
            
            return pygame.transform.scale(imagen, (self.ancho, self.alto))
            
        except Exception as e:
            print(f"Error cargando imagen: {str(e)}")
            print(f"Ruta intentada: {ruta}")
            # Crear placeholder con información de la carta
            superficie = pygame.Surface((self.ancho, self.alto))
            superficie.fill((30, 60, 30))  # Verde oscuro
            fuente = pygame.font.SysFont("Arial", 14)
            texto = fuente.render(f"{self.carta.valor} {self.carta.palo}", True, (255, 255, 255))
            superficie.blit(texto, (10, 60))
            return superficie

    def contiene_punto(self, pos):
        return (self.x <= pos[0] <= self.x + self.ancho and 
                self.y <= pos[1] <= self.y + self.alto)

    def dibujar(self, pantalla):
        imagen_a_dibujar = self.imagen
        
        # Aplicar rotación si es necesario
        if self.rotacion != 0:
            imagen_a_dibujar = pygame.transform.rotate(self.imagen, self.rotacion)
            # Ajustar posición para centrar la imagen rotada
            rect_original = self.imagen.get_rect()
            rect_rotado = imagen_a_dibujar.get_rect()
            offset_x = (rect_original.width - rect_rotado.width) // 2
            offset_y = (rect_original.height - rect_rotado.height) // 2
            pantalla.blit(imagen_a_dibujar, (self.x + offset_x, self.y + offset_y))
        else:
            pantalla.blit(imagen_a_dibujar, (self.x, self.y))
            
        if self.seleccionada:
            pygame.draw.rect(pantalla, (255, 215, 0), (self.x, self.y, self.ancho, self.alto), 3)