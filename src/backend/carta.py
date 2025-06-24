class carta:
    def __init__(self, palo=str, valor=int, nombre=str):
        """
        Clase que representa una carta de la baraja española.
        
        :param palo: El palo de la carta (bastos, copas, espadas, oros).
        :param valor: El valor de la carta (1-7,10,11,12).
        :param nombre: El nombre de la carta.
        """
        self.palo = palo
        self.valor = valor
        self.nombre = nombre

    def getPalo(self) -> str:
        """
        Retorna el palo de la carta.

        """
        return self.palo
    
    def getValor(self) -> int:
        """
        Retorna el valor de la carta.
        """
        return self.valor
    
    def getNombre(self) -> str:
        """
        Returns the name of the card.
        """
        palo = self.getPalo(carta)
        valor = self.getValor(carta)
        return f"{valor} de {palo}"