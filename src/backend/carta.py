class Carta:
    def __init__(self, palo: str, valor: str, puntos: int, imagen_path: str):
        self.palo = palo            # Ej: "Oros"
        self.valor = valor          # Ej: "As"
        self.puntos = puntos        # Ej: 11
        self.imagen_path = imagen_path  # Ruta para la GUI

    def __str__(self):
        return f"{self.valor} de {self.palo}"