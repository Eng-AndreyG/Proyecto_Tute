import pygame
import time
from src.frontend.componentes import CartaUI, BarajaUI, Boton
from src.backend.juego import Juego
from src.backend.ia import IAFacil, IAMedio, IADificil, IAStrategy
from src.backend.baza import Baza  
from src.backend.carta import Carta

class Partida:
    def __init__(self, pantalla, dificultad: str):
        self.pantalla = pantalla
        self.juego = Juego()
        self.juego.add_observer(self)  # Registrar esta partida como observer
        self.juego.iniciar_partida()
        self.juego.jugador_ia.estrategia = self._elegir_estrategia(dificultad)
        
        # Elementos UI
        self.baraja_ui = BarajaUI(50, 30)
        self.boton_tute = Boton(800, 650, 150, 50, "Cantar Tute", (200, 50, 50))
        self.fuente = pygame.font.SysFont("Arial", 24)
        
        # Estado del juego
        self.cartas_ui = []
        self.cartas_ia_ui = []
        self.cartas_en_juego = []
        self.cartas_ganadas_humano = []
        self.cartas_ganadas_ia = []
        self.mensaje_error = ""
        self.tiempo_mensaje = 0
        self.carta_arrastrando = None
        self.posicion_inicial_arrastre = None
        self.turno_ia_pendiente = False
        self.animacion_activa = False
        self.animacion_tiempo = 0
        self.resultado_baza = None
        
        self._inicializar_cartas()

    def mostrar_error(self, mensaje: str):
        """Muestra un mensaje de error temporal"""
        self.mensaje_error = mensaje
        self.tiempo_mensaje = pygame.time.get_ticks()

    def _inicializar_cartas(self):
        """Inicializa las cartas en UI y registra en IA"""
        self.cartas_ui = []
        self.cartas_ia_ui = []

        # Cartas IA (boca abajo)
        for i, carta in enumerate(self.juego.jugador_ia.mano):
            self.cartas_ia_ui.append(CartaUI(carta, 100 + i * 110, 50, visible=False))
            # Solo registrar cartas iniciales, no durante el juego
            if not hasattr(self, 'cartas_registradas_inicialmente'):
                if hasattr(self.juego.jugador_ia.estrategia, 'registrar_carta'):
                    self.juego.jugador_ia.estrategia.registrar_carta(carta)

        # Cartas Jugador (boca arriba)
        for i, carta in enumerate(self.juego.jugador_humano.mano):
            self.cartas_ui.append(CartaUI(carta, 100 + i * 110, 500, visible=True))

        self.cartas_registradas_inicialmente = True

    def _carta_ya_jugada(self, carta: Carta) -> bool: 
        """Verifica si una carta ya fue jugada"""
        if hasattr(self.juego.jugador_ia.estrategia, 'cartas_vistas'):
            return (carta.palo, carta.valor) in self.juego.jugador_ia.estrategia.cartas_vistas
        return False

    def manejar_eventos(self):
        if self.animacion_activa:
            return None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"

            if event.type == pygame.MOUSEBUTTONDOWN and not self.turno_ia_pendiente:
                if event.button == 1:  # Click izquierdo
                    for i, carta_ui in enumerate(self.cartas_ui):
                        if carta_ui.contiene_punto(event.pos):
                            self.carta_arrastrando = i
                            self.posicion_inicial_arrastre = (carta_ui.x, carta_ui.y)
                            carta_ui.seleccionada = True
                            break
                        
                if self.boton_tute.clickeado(event.pos):
                    if self._puede_cantar_tute():
                        if self._verificar_tute_valido():
                            self.juego.manejar_evento("tute_cantado")
                            return {"estado": "fin", "ganador": "humano"}
                        else:
                            self.mostrar_error("No tienes una combinación válida de Tute")
                    else:
                        self.mostrar_error("¡Necesitas 4 Reyes o 4 Caballos para cantar Tute!")

            elif event.type == pygame.MOUSEMOTION and self.carta_arrastrando is not None:
                carta_ui = self.cartas_ui[self.carta_arrastrando]
                carta_ui.x = event.pos[0] - carta_ui.ancho // 2
                carta_ui.y = event.pos[1] - carta_ui.alto // 2

            elif event.type == pygame.MOUSEBUTTONUP and self.carta_arrastrando is not None:
                if event.button == 1:
                    carta_idx = self.carta_arrastrando
                    carta_ui = self.cartas_ui[carta_idx]
                    carta_ui.seleccionada = False

                    # Obtener la carta del backend (no la UI)
                    carta_backend = self.juego.jugador_humano.mano[carta_idx]

                    # Verificar si la carta ya fue jugada (usando el objeto Carta real)
                    if (carta_backend.palo, carta_backend.valor) in self.juego.jugador_ia.estrategia.cartas_vistas:
                        self.mostrar_error("¡Esta carta ya fue jugada!")
                        if self.posicion_inicial_arrastre:
                            carta_ui.x, carta_ui.y = self.posicion_inicial_arrastre
                        continue

                    if self._es_zona_valida(event.pos):
                        try:
                            # Jugar carta del humano
                            carta_jugada = self.juego.jugador_humano.mano.pop(carta_idx)

                            # Registrar carta jugada en la estrategia IA
                            if hasattr(self.juego.jugador_ia.estrategia, 'registrar_carta'):
                                self.juego.jugador_ia.estrategia.registrar_carta(carta_jugada)

                            # Agregar a la baza
                            self.juego.baza_actual.agregar_carta("humano", carta_jugada)

                            # Mostrar en UI
                            self.cartas_en_juego.append((
                                "humano", 
                                CartaUI(carta_jugada, 400, 300, visible=True)
                            ))

                            # Actualizar mano
                            self._inicializar_cartas()

                            # Preparar turno IA
                            self.turno_ia_pendiente = True
                            self.animacion_tiempo = time.time()

                        except Exception as e:
                            self.mostrar_error(f"Error al jugar carta: {str(e)}")
                            if self.posicion_inicial_arrastre:
                                carta_ui.x, carta_ui.y = self.posicion_inicial_arrastre
                    else:
                        # Devolver carta a posición original si no se soltó en zona válida
                        if self.posicion_inicial_arrastre:
                            carta_ui.x, carta_ui.y = self.posicion_inicial_arrastre

                    # Resetear estado de arrastre
                    self.carta_arrastrando = None
                    self.posicion_inicial_arrastre = None

        return None

    def actualizar(self, evento: str = None):
        """Actualiza el estado del juego"""
        # Turno de IA
        if self.turno_ia_pendiente and len(self.cartas_en_juego) == 1 and time.time() - self.animacion_tiempo > 0.5:
            try:
                # Obtener carta de la IA
                carta_ia = self.juego.jugador_ia.jugar_carta(self.juego.baza_actual.palo_inicial)
                
                # Verificar que la carta existe en la mano de la IA
                if carta_ia not in self.juego.jugador_ia.mano:
                    raise ValueError("La IA intentó jugar una carta que no tiene")
                
                # Registrar y jugar la carta
                if hasattr(self.juego.jugador_ia.estrategia, 'registrar_carta'):
                    self.juego.jugador_ia.estrategia.registrar_carta(carta_ia)
                
                self.juego.baza_actual.agregar_carta("ia", carta_ia)
                self.juego.jugador_ia.mano.remove(carta_ia)  # Eliminar de la mano
                
                # Mostrar en UI
                self.cartas_en_juego.append(("ia", CartaUI(carta_ia, 400, 150, visible=True)))
                
                # Determinar ganador de la baza
                self.resultado_baza = self.juego.baza_actual.determinar_ganador()
                self.turno_ia_pendiente = False
                self.animacion_activa = True
                self.animacion_tiempo = time.time()
    
            except Exception as e:
                print(f"Error en turno IA: {e}")
                self.turno_ia_pendiente = False
                self.resultado_baza = "humano"  # Por defecto al humano si hay error
                self.animacion_activa = True
                self.animacion_tiempo = time.time()
    
        # Procesar baza completa
        if self.animacion_activa and len(self.cartas_en_juego) == 2 and time.time() - self.animacion_tiempo > 1.0:
            self.animacion_activa = False
            
            # Guardar cartas ganadas
            if self.resultado_baza == "humano":
                self.cartas_ganadas_humano.extend([c[1].carta for c in self.cartas_en_juego])
            else:
                self.cartas_ganadas_ia.extend([c[1].carta for c in self.cartas_en_juego])
            
            # Limpiar baza
            self.cartas_en_juego = []
            self.juego.baza_actual = Baza()
            self.juego.baza_actual.palo_triunfo = self.juego.palo_triunfo
            
            # Repartir nuevas cartas solo si hay en la baraja
            self._repartir_nuevas_cartas()
            
            # Verificar fin de partida (sin cartas en mano y no hay más para repartir)
            if (len(self.juego.jugador_humano.mano) == 0 and 
                len(self.juego.jugador_ia.mano) == 0 and
                len(self.juego.baraja.cartas) == 0):
                
                puntos_humano = sum(c.puntos for c in self.cartas_ganadas_humano)
                puntos_ia = sum(c.puntos for c in self.cartas_ganadas_ia)
                ganador = "humano" if puntos_humano > puntos_ia else "ia"
                return {"estado": "fin", "ganador": ganador}
    
        # Limpiar mensajes de error
        if self.mensaje_error and pygame.time.get_ticks() - self.tiempo_mensaje > 2000:
            self.mensaje_error = ""
    
        return None

    def _repartir_nuevas_cartas(self):
        """Reparte cartas solo si hay en la baraja y los jugadores necesitan"""
        # Solo repartir si hay cartas en la baraja
        if len(self.juego.baraja.cartas) > 0:
            # Repartir 1 carta a cada jugador si tienen menos de 8
            if len(self.juego.jugador_humano.mano) < 8:
                nuevas = self.juego.baraja.repartir(1)
                if nuevas:
                    self.juego.jugador_humano.mano.append(nuevas[0])

            if len(self.juego.jugador_ia.mano) < 8:
                nuevas = self.juego.baraja.repartir(1)
                if nuevas:
                    self.juego.jugador_ia.mano.append(nuevas[0])

            self._inicializar_cartas()

    def _es_zona_valida(self, pos) -> bool:
        return 300 <= pos[0] <= 700 and 250 <= pos[1] <= 450

    def _puede_cantar_tute(self) -> bool:
        mano = self.juego.jugador_humano.mano
        reyes = sum(1 for carta in mano if carta.valor == "Rey")
        caballos = sum(1 for carta in mano if carta.valor == "Caballo")
        return reyes == 4 or caballos == 4

    def _elegir_estrategia(self, dificultad: str):
        if dificultad == "facil":
            return IAFacil()
        elif dificultad == "medio":
            return IAMedio()
        elif dificultad == "dificil":
            return IADificil()
        return IAMedio()

    def dibujar(self):
        self.pantalla.fill((30, 90, 30))
        
        # Dibujar elementos
        self.baraja_ui.dibujar(self.pantalla)
        self.boton_tute.dibujar(self.pantalla)
        
        # Cartas en juego
        for jugador, carta_ui in self.cartas_en_juego:
            carta_ui.dibujar(self.pantalla)
        
        # Cartas de IA
        for carta in self.cartas_ia_ui:
            carta.dibujar(self.pantalla)
        
        # Cartas del jugador
        for carta in self.cartas_ui:
            carta.dibujar(self.pantalla)
        
        # Cartas ganadas
        for i, carta in enumerate(self.cartas_ganadas_humano[-8:]):
            carta_ui = CartaUI(carta, 50 + (i % 4) * 30, 350 - (i // 4) * 20, visible=True)
            carta_ui.dibujar(self.pantalla)
        
        for i, carta in enumerate(self.cartas_ganadas_ia[-8:]):
            carta_ui = CartaUI(carta, 800 + (i % 4) * 30, 150 - (i // 4) * 20, visible=True)
            carta_ui.dibujar(self.pantalla)
        
        # Mensajes
        if self.mensaje_error:
            texto = self.fuente.render(self.mensaje_error, True, (255, 0, 0))
            self.pantalla.blit(texto, (400, 300))
        
        pygame.display.flip()