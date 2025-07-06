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
        self.baraja_ui = BarajaUI(50, 280)  # Posición ajustada para la carta de triunfo
        self.boton_tute = Boton(800, 650, 150, 50, "Cantar Tute", (200, 50, 50))
        self.fuente = pygame.font.SysFont("Arial", 24)
        
        # Estado del juego
        self.cartas_ui = []
        self.cartas_ia_ui = []
        self.cartas_en_juego = []
        self.cartas_ganadas_humano = []
        self.cartas_ganadas_ia = []
        self.ultimo_ganador = None
        self.puntos_humano = 0
        self.puntos_ia = 0
        self.mensaje_error = ""
        self.tiempo_mensaje = 0
        self.carta_arrastrando = None
        self.posicion_inicial_arrastre = None
        self.turno_ia_pendiente = False
        self.animacion_activa = False
        self.animacion_tiempo = 0
        self.resultado_baza = None
        self.carta_triunfo_ui = None
        self.cache_imagenes_pequenas = {}  # Cache para imágenes escaladas
        
        self._inicializar_cartas()
        self._inicializar_carta_triunfo()
        
        # Debug: Verificar estado inicial
        print(f"=== NUEVA PARTIDA INICIADA ===")
        print(f"Humano: {len(self.juego.jugador_humano.mano)} cartas")
        print(f"IA: {len(self.juego.jugador_ia.mano)} cartas") 
        print(f"Baraja: {len(self.juego.baraja.cartas)} cartas")
        print(f"Palo triunfo: {self.juego.palo_triunfo}")
        print(f"=============================")

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

    def _inicializar_carta_triunfo(self):
        """Inicializa la carta de triunfo UI"""
        if hasattr(self.juego, 'carta_triunfo') and self.juego.carta_triunfo:
            # Posicionar corrida hacia la derecha de la baraja, en la misma altura
            x_triunfo = self.baraja_ui.x + 25  # Corrida hacia la derecha
            y_triunfo = self.baraja_ui.y       # Misma altura que la baraja
            self.carta_triunfo_ui = CartaUI(self.juego.carta_triunfo, x_triunfo, y_triunfo, visible=True)
            self.carta_triunfo_ui.rotacion = 90  # 90 grados en sentido horario

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
                            mensaje = f"¡Ganaste cantando Tute!\nPuntos finales: {self.puntos_humano} vs {self.puntos_ia}"
                            return {
                                "estado": "fin", 
                                "ganador": "humano", 
                                "puntos_humano": self.puntos_humano, 
                                "puntos_ia": self.puntos_ia,
                                "mensaje": mensaje
                            }
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
                            print(f"Jugador humano - Cartas antes: {len(self.juego.jugador_humano.mano)}")
                            
                            # Jugar carta del humano
                            carta_jugada = self.juego.jugador_humano.mano.pop(carta_idx)

                            print(f"Jugador humano - Cartas después: {len(self.juego.jugador_humano.mano)}")

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
                print(f"Turno IA - Cartas antes: {len(self.juego.jugador_ia.mano)}")
                print(f"Cartas IA: {[(c.palo, c.valor) for c in self.juego.jugador_ia.mano]}")
                
                # Obtener carta de la IA
                carta_ia = self.juego.jugador_ia.jugar_carta(self.juego.baza_actual.palo_inicial)
                print(f"IA eligió carta: {carta_ia.palo} {carta_ia.valor}")
                
                # Verificar que la carta existe en la mano de la IA
                if carta_ia not in self.juego.jugador_ia.mano:
                    print(f"ERROR: La carta {carta_ia.palo} {carta_ia.valor} no está en la mano de la IA!")
                    print(f"Mano actual: {[(c.palo, c.valor) for c in self.juego.jugador_ia.mano]}")
                    # Usar la primera carta disponible como fallback
                    if self.juego.jugador_ia.mano:
                        carta_ia = self.juego.jugador_ia.mano[0]
                        print(f"Usando carta fallback: {carta_ia.palo} {carta_ia.valor}")
                    else:
                        raise ValueError("La IA no tiene cartas en la mano")
                
                # Registrar y jugar la carta
                if hasattr(self.juego.jugador_ia.estrategia, 'registrar_carta'):
                    self.juego.jugador_ia.estrategia.registrar_carta(carta_ia)
                
                self.juego.baza_actual.agregar_carta("ia", carta_ia)
                self.juego.jugador_ia.mano.remove(carta_ia)  # Eliminar de la mano
                print(f"IA ahora tiene {len(self.juego.jugador_ia.mano)} cartas después de jugar")
                
                print(f"Turno IA - Cartas después: {len(self.juego.jugador_ia.mano)}")
                
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
            
            print(f"Finalizando baza - Ganador: {self.resultado_baza}")
            
            # Guardar cartas ganadas, calcular puntos y actualizar último ganador
            cartas_baza = [c[1].carta for c in self.cartas_en_juego]
            puntos_baza = sum(carta.puntos for carta in cartas_baza)
            
            if self.resultado_baza == "humano":
                self.cartas_ganadas_humano.extend(cartas_baza)
                self.puntos_humano += puntos_baza
                self.ultimo_ganador = "humano"
                print(f"Jugador humano gana {puntos_baza} puntos. Total: {self.puntos_humano}")
            else:
                self.cartas_ganadas_ia.extend(cartas_baza)
                self.puntos_ia += puntos_baza
                self.ultimo_ganador = "ia"
                print(f"IA gana {puntos_baza} puntos. Total: {self.puntos_ia}")
            
            print(f"Cartas ganadas - Humano: {len(self.cartas_ganadas_humano)}, IA: {len(self.cartas_ganadas_ia)}")
            print(f"Puntos actuales - Humano: {self.puntos_humano}, IA: {self.puntos_ia}")
            
            # Limpiar baza
            self.cartas_en_juego = []
            self.juego.baza_actual = Baza()
            self.juego.baza_actual.palo_triunfo = self.juego.palo_triunfo
            
            # Repartir nuevas cartas solo si hay en la baraja
            self._repartir_nuevas_cartas()
            
            # Verificar fin de partida (sin cartas en mano y no hay más para repartir)
            cartas_h = len(self.juego.jugador_humano.mano)
            cartas_i = len(self.juego.jugador_ia.mano)
            cartas_b = len(self.juego.baraja.cartas)
            
            print(f"VERIFICACIÓN FIN DE PARTIDA - Humano: {cartas_h}, IA: {cartas_i}, Baraja: {cartas_b}")
            
            if (cartas_h == 0 and cartas_i == 0 and cartas_b == 0):
                print("FIN DE PARTIDA DETECTADO")
                print(f"Puntos finales - Humano: {self.puntos_humano}, IA: {self.puntos_ia}")
                
                # Determinar ganador con lógica de desempate
                if self.puntos_humano > self.puntos_ia:
                    ganador = "humano"
                    mensaje = f"¡Ganaste! {self.puntos_humano} puntos vs {self.puntos_ia} puntos"
                elif self.puntos_ia > self.puntos_humano:
                    ganador = "ia"
                    mensaje = f"Gana la IA. {self.puntos_ia} puntos vs {self.puntos_humano} puntos"
                else:
                    # EMPATE - gana quien ganó la última baza
                    if hasattr(self, 'ultimo_ganador') and self.ultimo_ganador == "humano":
                        ganador = "humano"
                        mensaje = f"¡Empate en puntos! ({self.puntos_humano}-{self.puntos_ia})\nGanas por haber ganado la última baza"
                    else:
                        ganador = "ia"
                        mensaje = f"¡Empate en puntos! ({self.puntos_humano}-{self.puntos_ia})\nGana la IA por haber ganado la última baza"
                
                return {
                    "estado": "fin", 
                    "ganador": ganador, 
                    "puntos_humano": self.puntos_humano, 
                    "puntos_ia": self.puntos_ia,
                    "mensaje": mensaje
                }
    
        # Limpiar mensajes de error
        if self.mensaje_error and pygame.time.get_ticks() - self.tiempo_mensaje > 2000:
            self.mensaje_error = ""
    
        return None

    def _repartir_nuevas_cartas(self):
        """Reparte cartas manteniendo balance perfecto entre jugadores"""
        cartas_humano = len(self.juego.jugador_humano.mano)
        cartas_ia = len(self.juego.jugador_ia.mano)
        cartas_en_baraja = len(self.juego.baraja.cartas)
        
        print(f"Reparto - Humano: {cartas_humano}, IA: {cartas_ia}, Baraja: {cartas_en_baraja}")
        
        # Si no hay cartas en la baraja normal pero existe carta de triunfo, agregarla para robo final
        if cartas_en_baraja == 0 and hasattr(self.juego, 'carta_triunfo') and self.juego.carta_triunfo:
            if not hasattr(self, 'triunfo_agregado'):
                print("Agregando carta de triunfo de vuelta a la baraja para robo final")
                self.juego.baraja.cartas.append(self.juego.carta_triunfo)
                self.triunfo_agregado = True
                cartas_en_baraja = 1
        
        # Repartir cartas mientras hay disponibles y alguien necesita
        if cartas_en_baraja > 0:
            # Si ambos necesitan cartas
            if cartas_humano < 8 and cartas_ia < 8:
                if cartas_en_baraja >= 2:
                    # Dar una carta a cada uno
                    nueva_humano = self.juego.baraja.repartir(1)
                    if nueva_humano:
                        self.juego.jugador_humano.mano.append(nueva_humano[0])
                        print(f"Carta dada al humano")
                    
                    nueva_ia = self.juego.baraja.repartir(1)
                    if nueva_ia:
                        self.juego.jugador_ia.mano.append(nueva_ia[0])
                        print(f"Carta dada a la IA")
                        
                elif cartas_en_baraja == 1:
                    # Solo queda una carta, dársela al ganador de la baza
                    nueva = self.juego.baraja.repartir(1)
                    if nueva:
                        if hasattr(self, 'ultimo_ganador') and self.ultimo_ganador == "ia":
                            self.juego.jugador_ia.mano.append(nueva[0])
                            print(f"Última carta dada a la IA (ganó la baza)")
                        else:
                            self.juego.jugador_humano.mano.append(nueva[0])
                            print(f"Última carta dada al humano (ganó la baza)")
            
            # Si solo el humano necesita cartas
            elif cartas_humano < 8:
                nueva = self.juego.baraja.repartir(1)
                if nueva:
                    self.juego.jugador_humano.mano.append(nueva[0])
                    print(f"Carta dada al humano")
            
            # Si solo la IA necesita cartas
            elif cartas_ia < 8:
                nueva = self.juego.baraja.repartir(1)
                if nueva:
                    self.juego.jugador_ia.mano.append(nueva[0])
                    print(f"Carta dada a la IA")

        self._inicializar_cartas()
        
        # Actualizar carta de triunfo si ya no hay cartas
        if len(self.juego.baraja.cartas) == 0:
            self.carta_triunfo_ui = None
            
        print(f"Cartas después del reparto - Humano: {len(self.juego.jugador_humano.mano)}, IA: {len(self.juego.jugador_ia.mano)}, Baraja: {len(self.juego.baraja.cartas)}")

    def _es_zona_valida(self, pos) -> bool:
        return 300 <= pos[0] <= 700 and 250 <= pos[1] <= 450

    def _puede_cantar_tute(self) -> bool:
        mano = self.juego.jugador_humano.mano
        reyes = sum(1 for carta in mano if carta.valor == "Rey")
        caballos = sum(1 for carta in mano if carta.valor == "Caballo")
        return reyes == 4 or caballos == 4

    def _verificar_tute_valido(self) -> bool:
        """Verifica si realmente tiene 4 reyes o 4 caballos para el Tute"""
        return self._puede_cantar_tute()  # Si puede cantar, es válido

    def _elegir_estrategia(self, dificultad: str):
        if dificultad == "facil":
            return IAFacil()
        elif dificultad == "medio":
            return IAMedio()
        elif dificultad == "dificil":
            return IADificil()
        return IAMedio()

    def _obtener_imagen_pequena(self, carta, escala=0.6):
        """Obtiene una imagen escalada de la carta, usando cache para optimización"""
        key = (carta.palo, carta.valor, escala)
        if key not in self.cache_imagenes_pequenas:
            carta_temp = CartaUI(carta, 0, 0, visible=True)
            ancho = int(100 * escala)
            alto = int(150 * escala)
            self.cache_imagenes_pequenas[key] = pygame.transform.scale(carta_temp.imagen, (ancho, alto))
        return self.cache_imagenes_pequenas[key]

    def dibujar(self):
        self.pantalla.fill((30, 90, 30))
        
        # Dibujar baraja y carta de triunfo solo si hay cartas para robar
        if len(self.juego.baraja.cartas) > 0:
            # Dibujar carta de triunfo PRIMERO (abajo en Z)
            if self.carta_triunfo_ui:
                self.carta_triunfo_ui.dibujar(self.pantalla)
            
            # Dibujar baraja ENCIMA de la carta de triunfo
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
        
        # Cartas ganadas del jugador (amontonadas como baraja debajo de sus cartas)
        if self.cartas_ganadas_humano:
            base_x = 100  # Posición base
            base_y = 680  # Debajo de las cartas del jugador
            for i, carta in enumerate(self.cartas_ganadas_humano):
                # Crear efecto de amontonamiento con pequeños offsets
                offset_x = i * 2  # Pequeño desplazamiento horizontal
                offset_y = i * 1  # Pequeño desplazamiento vertical
                x = base_x + offset_x
                y = base_y + offset_y
                
                # Usar imagen en caché
                imagen_pequena = self._obtener_imagen_pequena(carta, 0.5)
                self.pantalla.blit(imagen_pequena, (x, y))
        
        # Cartas ganadas de la IA (amontonadas en cuadrante superior derecho)
        if self.cartas_ganadas_ia:
            base_x = 800  # Cuadrante superior derecho
            base_y = 150  # Segunda fila de cuadrícula
            for i, carta in enumerate(self.cartas_ganadas_ia):
                # Crear efecto de amontonamiento con pequeños offsets
                offset_x = i * 2  # Pequeño desplazamiento horizontal
                offset_y = i * 1  # Pequeño desplazamiento vertical
                x = base_x + offset_x
                y = base_y + offset_y
                
                # Usar imagen en caché
                imagen_pequena = self._obtener_imagen_pequena(carta, 0.5)
                self.pantalla.blit(imagen_pequena, (x, y))
        
        # Mostrar puntuación en tiempo real
        fuente_puntos = pygame.font.SysFont("Arial", 20, bold=True)
        
        # Puntos del jugador humano (abajo a la izquierda)
        texto_puntos_humano = fuente_puntos.render(f"Tus puntos: {self.puntos_humano}", True, (255, 255, 255))
        self.pantalla.blit(texto_puntos_humano, (10, 730))
        
        # Puntos de la IA (arriba a la derecha)
        texto_puntos_ia = fuente_puntos.render(f"IA: {self.puntos_ia}", True, (255, 255, 255))
        self.pantalla.blit(texto_puntos_ia, (850, 10))
        
        # Mostrar el palo de triunfo
        if hasattr(self.juego, 'palo_triunfo') and self.juego.palo_triunfo:
            texto_triunfo = fuente_puntos.render(f"Triunfo: {self.juego.palo_triunfo}", True, (255, 215, 0))
            self.pantalla.blit(texto_triunfo, (10, 10))
        
        # Mensajes
        if self.mensaje_error:
            texto = self.fuente.render(self.mensaje_error, True, (255, 0, 0))
            self.pantalla.blit(texto, (400, 300))
        
        pygame.display.flip()