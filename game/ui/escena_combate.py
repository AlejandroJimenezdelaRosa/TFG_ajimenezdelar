import pygame
import math
import random
from moviepy import VideoFileClip

SET_LICORES = ["Anís", "Pacharán", "Orujo", "Vermut"]

# ============================================================
# ESCENA DEL COMBATE
# ============================================================
class EscenaCombate:
    def __init__(self, partida):
        self.partida = partida
        self.partida.escena = self 
        self.jugador = partida.jugador
        self.rival = partida.rival
        self.cartas_elevadas = []
        self.zoom_activo = False
        self.fade_surface = pygame.Surface((1280, 720))
        self.fade_surface.fill((0, 0, 0))
        self._fin_timestamp = 0

        # ICONO DE AYUDA (ESCALADO PARA QUE SE VEA BIEN) 
        icono_original = pygame.image.load("game/ui/assets/objetos/help.png").convert_alpha()
        self.icono_ayuda = pygame.transform.smoothscale(icono_original, (24, 32))  # tamaño pequeño, NO tocar más
        self.rect_icono_ayuda = self.icono_ayuda.get_rect()

        # =======================================================
        # TEXTO DEL RECUADRO (SOLO ÚLTIMO MENSAJE DE LA ACCIÓM)
        # =======================================================
        self.texto_accion_completo = ""
        self.texto_accion_visible = ""
        self.texto_accion_tiempo = 0
        self.texto_accion_velocidad = 30  # caracteres por segundo
        self.texto_accion_alpha = 0
        self.font_accion = pygame.font.SysFont("Arial", 18)

        # Turnos 
        self.turno = "jugador"
        self.numero_turno = 1
        self.turno_global = 1
        self.texto_turno = f"Turno {self.numero_turno}"
        self.texto_accion = ""
        self.ancho, self.alto = 1280, 720

        # ===========================
        # MAZO E IMÁGEN DEL REVERSO
        # ==========================
        try:
            self.img_mazo = pygame.image.load("game/ui/assets/mazo.png").convert_alpha()
            self.img_mazo = pygame.transform.scale(self.img_mazo, (120, 160))
        except:
            self.img_mazo = pygame.Surface((120, 160))
            self.img_mazo.fill((50, 20, 10))

        self.img_reverso = pygame.transform.scale(self.img_mazo, (96, 135))
        self.pos_mazo = (40, self.alto // 2 - 80)

        # ============
        # ESCENARIOS
        # =============
        self.mesa_surface = pygame.Surface((self.ancho, self.alto))
        self.mesa_surface.fill((90, 60, 30))
        self.oponente_surface = pygame.Surface((300, 260), pygame.SRCALPHA)
        self.oponente_surface.fill((60, 60, 60))
        pygame.draw.rect(self.oponente_surface, (220, 220, 220), (10, 10, 280, 240), 3)

        # =============================================
        # MANO CON LAS CARTAS DEL JUGADOR Y DEL RIVAL
        # =============================================
        self.cartas_jugador = self.jugador.mano
        self.cartas_rival = self.rival.mano
        self.carta_seleccionada = 0
        self.ultima_carta = None
        self.pos_cartas_jugador = []
        self.pos_cartas_rival = []

        # Turno
        self.turno = "jugador"
        self.numero_turno = 1
        self._jugador_ya_robo = True
        self._rival_ya_robo = True

        # ZOOM para ver la carta en grande
        self.zoom_card = None
        self.zoom_card_img = None
        self.zoom_card_rect = None

        # Texto de la carta para saber que coño hace
        self.textbox_font = pygame.font.SysFont("Arial", 26)
        self.textbox_desc_font = pygame.font.SysFont("Arial", 22)
        self.texto_turno = f"Turno {self.numero_turno}"

        # Teclas de las cartas
        self._tecla_left_prev = False
        self._tecla_right_prev = False
        self._tecla_enter_prev = False
        self._tecla_esc_prev = False

        # Confirmar la carta usada
        self.confirmar_opciones = ["Sí", "No"]
        self.confirmar_seleccion = 0
        self.carta_pendiente = None

        # ====================================================
        # VIDEO Y TRANSICIÓN
        # ====================================================
        self.estado = "pre_video_fade_in"
        self.fade_alpha = 255  # empieza en negro

        self.video_vs = VideoFileClip("game/ui/assets/videos/vs_intro.mp4")
        self.video_time = 0
        self.video_duration = self.video_vs.duration * 1000
        self.video_fps = self.video_vs.fps

        pygame.mixer.init()
        self.vs_audio = pygame.mixer.Sound("game/ui/assets/videos/vs_intro_audio.mp3")
        self.vs_audio_played = False
        self._last_tick = pygame.time.get_ticks()
        self.recalcular_posiciones()

        # ===================
        # SONIDOS DEL JUEGO
        # ====================
        self.sonidos = {
            "critico": pygame.mixer.Sound("game/ui/assets/sonidos/critico.wav"),
            "evento": pygame.mixer.Sound("game/ui/assets/sonidos/evento.wav"),
            "estado_contentillo": pygame.mixer.Sound("game/ui/assets/sonidos/estado_contentillo.wav"),
            "estado_tocado": pygame.mixer.Sound("game/ui/assets/sonidos/estado_tocado.wav"),
            "estado_ciego": pygame.mixer.Sound("game/ui/assets/sonidos/estado_ciego.wav"),
        }

    # ==================
    # VIDEO VS RIVAL
    # ===================
    def reproducir_video_vs(self, window, dt):
        if not self.vs_audio_played:
            self.vs_audio.play()
            self.vs_audio_played = True
        self.video_time += dt

        if self.video_time >= self.video_duration:
            self.video_vs.close()
            self.vs_audio.stop()
            self.fade_alpha = 0
            self.estado = "post_video_fade_out"
            return

        frame = self.video_vs.get_frame(self.video_time / 1000.0)
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        frame_surface = pygame.transform.scale(frame_surface, (self.ancho, self.alto))
        window.blit(frame_surface, (0, 0))

    def fade_in_pre_video(self, window, dt):
        self.fade_alpha -= dt * 0.2
        if self.fade_alpha < 0:
            self.fade_alpha = 0
            self.estado = "video_vs"
            return

        panel = pygame.Surface((self.ancho, self.alto))
        panel.fill((0, 0, 0))
        panel.set_alpha(int(self.fade_alpha))
        window.blit(panel, (0, 0))

    def fade_out_post_video(self, window, dt):
        self.fade_alpha += dt * 0.2
        if self.fade_alpha >= 255:
            self.fade_alpha = 255
            self.estado = "inicio_turno"
            return

        panel = pygame.Surface((self.ancho, self.alto))
        panel.fill((0, 0, 0))
        panel.set_alpha(int(self.fade_alpha))
        window.blit(panel, (0, 0))

    # =============
    # POSICIONES
    # ==============
    def recalcular_posiciones(self):
        if len(self.cartas_jugador) == 0:
            self.carta_seleccionada = 0
        else:
            self.carta_seleccionada = min(self.carta_seleccionada, len(self.cartas_jugador) - 1)

        n_j = max(1, len(self.cartas_jugador))
        total_ancho_j = n_j * 90
        inicio_x_j = (self.ancho - total_ancho_j) // 2

        self.pos_cartas_jugador = [
            (inicio_x_j + i * 90, 520) for i in range(len(self.cartas_jugador))
        ]

        n_r = max(1, len(self.cartas_rival))
        total_ancho_r = n_r * 90
        inicio_x_r = (self.ancho - total_ancho_r) // 2

        self.pos_cartas_rival = [
            (inicio_x_r + i * 90, 80) for i in range(len(self.cartas_rival))
        ]

    # ===================================
    # SELECCIONAR LA CARTA
    # ==================================
    def detectar_hover(self):
        if self.estado != "seleccion":
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for i, carta in enumerate(self.cartas_jugador):
            x, y = self.pos_cartas_jugador[i]
            rect = pygame.Rect(x, y, 96, 135)
            if rect.collidepoint(mouse_x, mouse_y):
                self.carta_seleccionada = i
                return

    def reproducir_sonido(self, nombre):
        try:
            if nombre in self.sonidos:
                self.sonidos[nombre].play()
        except:
            pass

    # ========
    # ZOOM
    # ========
    def actualizar_zoom_card(self):
        if not self.zoom_activo:
            self.zoom_card = None
            self.zoom_card_img = None
            self.zoom_card_rect = None
            return

        if self.cartas_jugador and 0 <= self.carta_seleccionada < len(self.cartas_jugador):
            self.zoom_card = self.cartas_jugador[self.carta_seleccionada]
            self.zoom_card_img = self.zoom_card.img_big
            self.zoom_card_rect = self.zoom_card_img.get_rect(
                center=(self.ancho // 2, self.alto // 2 - 60)
            )
        else:
            self.zoom_card = None
            self.zoom_card_img = None
            self.zoom_card_rect = None

    def draw_zoom_card(self, window):
        if self.zoom_card_img:
            window.blit(self.zoom_card_img, self.zoom_card_rect)

    # ===================
    # TEXTO DE LA CARTA
    # ====================
    def draw_textbox(self, window):
        if not self.zoom_card:
            return

        panel_h = 200
        panel = pygame.Surface((self.ancho, panel_h), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 200))
        window.blit(panel, (0, self.alto - panel_h))
        carta = self.zoom_card
        nombre = self.textbox_font.render(
            f"{carta.nombre} ({carta.tipo})", True, (255, 255, 0)
        )
        window.blit(nombre, (40, self.alto - panel_h + 20))

        y = self.alto - panel_h + 60
        for linea in carta.descripcion.split("\n"):
            t = self.textbox_desc_font.render(linea, True, (220, 220, 220))
            window.blit(t, (40, y))
            y += 24

    # ============================================
    # PUNTOS DE ALCOHOL (LA BARRA DE BORRACHERA)
    # ============================================
    def draw_barras(self, window):
        ancho_barra = 250
        alto_barra = 25
        color_fondo = (40, 20, 10)
        color_marco = (255, 255, 255)
        color_cerveza = (230, 180, 40)

        font = pygame.font.SysFont("Arial", 22)
        max_borracha = 100

        # La del rival
        x_r = 40
        y_r = 40
        pygame.draw.rect(window, color_marco, (x_r - 2, y_r - 2, ancho_barra + 4, alto_barra + 4), 2)
        pygame.draw.rect(window, color_fondo, (x_r, y_r, ancho_barra, alto_barra))
        p_r = max(0.0, min(1.0, self.rival.borracha / max_borracha))
        pygame.draw.rect(window, color_cerveza, (x_r, y_r, int(ancho_barra * p_r), alto_barra))
        texto_r = font.render(self.rival.nombre, True, (255, 255, 255))
        window.blit(texto_r, (x_r, y_r + alto_barra + 8))

        # La del jugador
        x_j = self.ancho - ancho_barra - 40
        y_j = self.alto - alto_barra - 40
        pygame.draw.rect(window, color_marco, (x_j - 2, y_j - 2, ancho_barra + 4, alto_barra + 4), 2)
        pygame.draw.rect(window, color_fondo, (x_j, y_j, ancho_barra, alto_barra))
        p_j = max(0.0, min(1.0, self.jugador.borracha / max_borracha))
        pygame.draw.rect(window, color_cerveza, (x_j, y_j, int(ancho_barra * p_j), alto_barra))
        texto_j = font.render(self.jugador.nombre, True, (255, 255, 255))
        window.blit(texto_j, (x_j, y_j - 28))

    # ============================
    # CONFIRMAR LA CARTA A USAR
    # ============================
    def draw_confirmacion(self, window):
        ancho = 500
        alto = 140
        x = (self.ancho - ancho) // 2
        y = self.alto - alto - 40

        panel = pygame.Surface((ancho, alto))
        panel.fill((240, 240, 240))
        pygame.draw.rect(panel, (0, 0, 0), (0, 0, ancho, alto), 3)

        font = pygame.font.SysFont("Arial", 24)
        pregunta = font.render(f'¿Usar "{self.carta_pendiente.nombre}"?', True, (0, 0, 0))
        panel.blit(pregunta, (20, 20))
        for i, txt in enumerate(self.confirmar_opciones):
            t = font.render(txt, True, (0, 0, 0))
            tx = 80 + i * 140
            ty = 80
            panel.blit(t, (tx, ty))
            if i == self.confirmar_seleccion:
                pygame.draw.polygon(
                    panel,
                    (0, 0, 0),
                    [(tx - 20, ty + 4), (tx - 8, ty + 12), (tx - 20, ty + 20)]
                )
        window.blit(panel, (x, y))

    # ============================================================
    # TEXTO DEL RECUADRO (SOLO ÚLTIMO MENSAJE DE LA ACCIÓM)
    # ============================================================
    def iniciar_texto_accion(self, texto):
        # Guardar texto
        self.texto_accion_completo = texto
        self.texto_accion_visible = ""
        self.texto_accion_tiempo = pygame.time.get_ticks()
        self.texto_accion_alpha = 255

        # bloquear el combate mientras hay texto
        self.estado_anterior = self.estado
        self.estado = "texto"

    def actualizar_texto_accion(self):
        if not self.texto_accion_completo:
            return
        ahora = pygame.time.get_ticks()
        tiempo = (ahora - self.texto_accion_tiempo) / 1000.0

        # Efecto máquina de escribir
        chars = int(tiempo * self.texto_accion_velocidad)
        self.texto_accion_visible = self.texto_accion_completo[:chars]

        # Transición después de 5 segundos
        if tiempo > 5:
            self.texto_accion_alpha -= 4
            if self.texto_accion_alpha <= 0:
                # Texto terminado
                self.texto_accion_completo = ""
                self.texto_accion_visible = ""
                self.texto_accion_alpha = 0

                # Restaurar estado anterior
                if self.estado == "texto":
                    self.estado = self.estado_anterior

    # ==========================
    # LÓGICA PARA EL JUGADOR
    # ==========================
    def logica_inicio_turno(self):
        self.texto_turno = f"Turno {self.numero_turno}"
        if random.random() < 0.15:
            from mazos import evento_del_bar
            self.reproducir_sonido("evento")
            evento_del_bar(self.partida, self.jugador, self.rival)

        # Si el jugador pierde el turno por evento del bar
        if self.jugador.pasar_turno_flag:
            self.partida.narrar(f"{self.jugador.nombre} pierde el turno.")
            self.jugador.pasar_turno_flag = False
            self._jugador_ya_robo = False
            self.estado = "rival"
            return

        if not self._jugador_ya_robo:
            self.jugador.robar(self.partida.mazo_central, 1, partida=self.partida)
            self.cartas_jugador = list(self.jugador.mano) 
            self._jugador_ya_robo = True
        self.estado = "seleccion"

    def logica_seleccion(self, keys):
        left = keys[pygame.K_LEFT]
        right = keys[pygame.K_RIGHT]
        enter = keys[pygame.K_RETURN]
        esc = keys[pygame.K_ESCAPE]

        # Flechas para moverse
        if left and not self._tecla_left_prev:
            self.carta_seleccionada = max(0, self.carta_seleccionada - 1)
        if right and not self._tecla_right_prev:
            self.carta_seleccionada = min(len(self.cartas_jugador) - 1, self.carta_seleccionada + 1)

        # SHIFT o clic derecho provoca el zoom
        shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        right_click = pygame.mouse.get_pressed()[2]
        self.zoom_activo = shift or right_click

        # CLICK IZQUIERDO para seleccionar / elevar / jugar
        mouse_left = pygame.mouse.get_pressed()[0]
        if mouse_left and not getattr(self, "_mouse_prev", False):
            mx, my = pygame.mouse.get_pos()
            for i, (x, y) in enumerate(self.pos_cartas_jugador):
                rect = pygame.Rect(x, y - 20, 96, 135)
                if rect.collidepoint(mx, my):
                    carta = self.cartas_jugador[i]
                    self.carta_seleccionada = i

                    if carta in self.cartas_elevadas:
                        # Ya estaba elevada, jugar
                        if len(self.cartas_elevadas) > 1:
                            self.intentar_jugar()
                        else:
                            self.carta_pendiente = carta
                            self.cartas_elevadas.remove(carta)
                            self.ejecutar_carta_pendiente()
                    else:
                        # Primera pulsación, elevar
                        self.cartas_elevadas.append(carta)
                    break
        self._mouse_prev = mouse_left

        # ENTER para seleccionar o confirmar
        if enter and not self._tecla_enter_prev:
            # Evitar cuelgue si no hay cartas jugables
            if not self.cartas_jugador:
                self.texto_turno = "No tienes cartas jugables."
                return
            carta = self.cartas_jugador[self.carta_seleccionada]

            if carta in self.cartas_elevadas:
                if len(self.cartas_elevadas) > 1:
                    self.intentar_jugar()
                    self._tecla_enter_prev = enter
                    return

                self.carta_pendiente = carta
                self.cartas_elevadas.remove(carta)
                self.ejecutar_carta_pendiente()
                self._tecla_enter_prev = enter
                return

            self.cartas_elevadas.append(carta)

        # ESC para cancelar la selección o pasar turno
        if esc and not self._tecla_esc_prev:
            if self.cartas_elevadas:
                self.cartas_elevadas = []
            else:
                self.partida.narrar(f"{self.jugador.nombre} decide pasar turno.")
                self.iniciar_texto_accion(f"{self.jugador.nombre} pasó turno.")
                self.texto_turno = f"{self.jugador.nombre} pasó turno."
                self._jugador_ya_robo = False
                self.estado = "rival"

        self._tecla_left_prev = left
        self._tecla_right_prev = right
        self._tecla_enter_prev = enter
        self._tecla_esc_prev = esc

    # ==================================
    # COMBOS CON LAS CARTAS DE SET 
    # ==================================
    def validar_combo(self, cartas):
        # Deben ser todas tipo set
        if not all(c.tipo.lower() == "set" for c in cartas):
            return False
        nombres = [c.nombre for c in cartas]
        unicos = set(nombres)

        # Pareja (2 iguales)
        if len(cartas) == 2 and len(unicos) == 1:
            return True

        # Trío (3 iguales)
        if len(cartas) == 3 and len(unicos) == 1:
            return True

        # Set completo (1 de cada licor)
        if len(cartas) == len(SET_LICORES) and all(n in nombres for n in SET_LICORES):
            return True

        # Set incompleto (3 licores distintos)
        if len(cartas) == 3:
            nombres_unicos = {c.nombre for c in cartas}
            if all(n in SET_LICORES for n in nombres_unicos) and len(nombres_unicos) == 3:
                return True
        return False

    def intentar_jugar(self):
        # Si solo hay una carta elevada, se juga normalmente
        if len(self.cartas_elevadas) == 1:
            self.carta_pendiente = self.cartas_elevadas[0]
            self.cartas_elevadas = []
            self.ejecutar_carta_pendiente()
            return

        # Si hay varias cartas elevadas
        if len(self.cartas_elevadas) > 1:

            # 1) Si TODAS son tipo set, usar la lógica de los combos SET
            if all(c.tipo.lower() == "set" for c in self.cartas_elevadas):
                if self.validar_combo(self.cartas_elevadas):
                    self.carta_pendiente = self.cartas_elevadas[0]
                    self.cartas_elevadas = []
                    self.ejecutar_carta_pendiente()
                    return
                else:
                    self.texto_turno = "Esa combinación no es válida."
                    self.cartas_elevadas = []
                    return

            # 2) Sinergias: 1 carta principal + 1 carta de set
            no_sets = [c for c in self.cartas_elevadas if c.tipo.lower() != "set"]
            sets = [c for c in self.cartas_elevadas if c.tipo.lower() == "set"]

            # Caso de 1 carta principal + 1 set
            if len(no_sets) == 1 and len(sets) == 1:
                carta_principal = no_sets[0]
                carta_set = sets[0]

                # Consumir la carta de set
                if carta_set in self.jugador.mano:
                    self.jugador.mano.remove(carta_set)
                if carta_set in self.cartas_jugador:
                    self.cartas_jugador.remove(carta_set)

                # Jugar la carta principal
                self.carta_pendiente = carta_principal
                self.cartas_elevadas = []
                self.ejecutar_carta_pendiente()
                return

            # Si hay más de una carta principal será inválido
            self.texto_turno = "Esa combinación no es válida."
            self.cartas_elevadas = []
            return

        # Si no hay cartas elevadas
        self.texto_turno = "No has seleccionado ninguna carta."

    def logica_confirmar(self, keys):
        left = keys[pygame.K_LEFT]
        right = keys[pygame.K_RIGHT]
        enter = keys[pygame.K_RETURN]
        esc = keys[pygame.K_ESCAPE]

        if left and not self._tecla_left_prev:
            self.confirmar_seleccion = (self.confirmar_seleccion - 1) % len(self.confirmar_opciones)
        if right and not self._tecla_right_prev:
            self.confirmar_seleccion = (self.confirmar_seleccion + 1) % len(self.confirmar_opciones)

        if enter and not self._tecla_enter_prev:
            opcion = self.confirmar_opciones[self.confirmar_seleccion]
            if opcion == "Sí":
                self.ejecutar_carta_pendiente()
                return
            else:
                self.estado = "seleccion"

        if esc and not self._tecla_esc_prev:
            self.estado = "seleccion"

        self._tecla_left_prev = left
        self._tecla_right_prev = right
        self._tecla_enter_prev = enter
        self._tecla_esc_prev = esc

    def ejecutar_carta_pendiente(self):
        if not self.carta_pendiente:
            self.estado = "seleccion"
            return

        carta = self.carta_pendiente
        if carta not in self.cartas_jugador:
            self.estado = "seleccion"
            return

        self.ultima_carta = carta
        self.iniciar_texto_accion(f"{self.jugador.nombre} usó {carta.nombre}")
        carta.usar(self.jugador, self.rival, self.partida)
        self.jugador.aplicar_sinergias(carta, self.rival, self.partida)

        # Mostrar texto ESPECIAL si corresponde
        if getattr(carta, "tipo", "").lower() == "especial":
            self.iniciar_texto_accion("¡ESPECIAL!")

        # Activar combo ANTES de eliminar la carta de la mano
        self.jugador.activar_combo_auto(self.rival, self.partida)

        # Sincronizar mano tras posibles combos
        self.cartas_jugador = list(self.jugador.mano)

        if self.jugador.combo_activado:
            # Primero mensaje de haber efectuado un combo
            self.iniciar_texto_accion("¡COMBO!")
            # Luego el texto concreto del combo 
            self.iniciar_texto_accion(self.jugador.ultimo_texto_combo)

        # Eliminar la carta jugada de la mano lógica y visual
        if carta in self.jugador.mano:
            self.jugador.mano.remove(carta)
        if carta in self.cartas_jugador:
            self.cartas_jugador.remove(carta)

        self.carta_pendiente = None

        if len(self.cartas_jugador) == 0:
            self.carta_seleccionada = 0
        else:
            self.carta_seleccionada = min(self.carta_seleccionada, len(self.cartas_jugador) - 1)

        self.jugador.aplicar_efectos(self.partida)
        self.rival.aplicar_efectos(self.partida)
        self.jugador.mensaje_estado(self.partida)
        self.rival.mensaje_estado(self.partida)

        if self.partida.comprobar_fin():
            # Mensaje general
            if self.partida.resultado == "victoria":
                self.iniciar_texto_accion("¡Victoria! Has dejado KO al rival.")
            else:
                self.iniciar_texto_accion("Derrota... Te has pasado de borrachera.")

            # Frase personalizada del rival
            frase = getattr(self.rival, "frase_derrota", None) if self.partida.resultado == "victoria" else getattr(self.rival, "frase_victoria", None)
            if frase:
                self.iniciar_texto_accion(frase)

            # Activar estado final
            self.estado = "fin"
            self._fin_timestamp = pygame.time.get_ticks()
            return

        self.turno_global += 1
        self._jugador_ya_robo = False
        self.estado = "rival"

    # =======================
    # LÓGICA DEL RIVAL
    # ======================
    def logica_rival(self):
        self.texto_turno = f"Turno {self.numero_turno} — {self.rival.nombre} actúa..."
        if random.random() < 0.15:
            from mazos import evento_del_bar
            self.reproducir_sonido("evento")
            evento_del_bar(self.partida, self.rival, self.jugador)

        if self.rival.pasar_turno_flag:
            self.partida.narrar(f"{self.rival.nombre} pierde el turno.")
            self.rival.pasar_turno_flag = False
            self.numero_turno += 1
            self.turno_global += 1
            self._rival_ya_robo = False
            self.estado = "inicio_turno"
            return

        if not self._rival_ya_robo:
            self.rival.robar(self.partida.mazo_central, 1, partida=self.partida)
            self.cartas_rival = list(self.rival.mano)   # ← SINCRONIZACIÓN
            self._rival_ya_robo = True

        self.partida.narrar(f"{self.rival.nombre} está pensando...")

        self.jugador.aplicar_efectos(self.partida)
        self.rival.aplicar_efectos(self.partida)

        # Combo del rival
        hizo_combo = self.rival.activar_combo_auto(self.jugador, self.partida)
        # Sincronizar mano del rival tras posibles combos
        self.cartas_rival = list(self.rival.mano)

        if hizo_combo:
            self.iniciar_texto_accion(self.rival.ultimo_texto_combo)

        if not hizo_combo and self.cartas_rival:
            carta = self.cartas_rival[0]
            self.ultima_carta = carta

            # Mensaje principal del recuadro
            self.iniciar_texto_accion(f"{self.rival.nombre} usó {carta.nombre}")
            self.texto_turno = f"¡{self.rival.nombre} usó {carta.nombre}!"

            # Usar carta
            carta.usar(self.rival, self.jugador, self.partida)

            # Eliminar de la mano lógica y visual
            if carta in self.rival.mano:
                self.rival.mano.remove(carta)
            if carta in self.cartas_rival:
                self.cartas_rival.remove(carta)

        self.jugador.mensaje_estado(self.partida)
        self.rival.mensaje_estado(self.partida)

        if self.partida.comprobar_fin():

            # Mensaje general
            if self.partida.resultado == "victoria":
                self.iniciar_texto_accion("¡Victoria! Has dejado KO al rival.")
            else:
                self.iniciar_texto_accion("Derrota... Te has pasado de borrachera.")

            # Frase personalizada del rival
            frase = getattr(self.rival, "frase_derrota", None) if self.partida.resultado == "victoria" else getattr(self.rival, "frase_victoria", None)
            if frase:
                self.iniciar_texto_accion(frase)

            # Activar estado final
            self.estado = "fin"
            self._fin_timestamp = pygame.time.get_ticks()
            return

        self.numero_turno += 1
        self.turno_global += 1
        self._rival_ya_robo = False
        self.estado = "inicio_turno"
        return None

    # ====================
    # UPDATE PRINCIPAL
    # ====================
    def update(self, window, keys):
        now = pygame.time.get_ticks()
        dt = now - self._last_tick
        self._last_tick = now

        # ====================================================================================
        # SI EL COMBATE YA HA TERMINADO SE HACE TRANSICIÓN A NEGRO Y SE DEVUELVE EL RESULTADO
        # ====================================================================================
        if self.estado == "fin":
            self.actualizar_texto_accion()
            self.draw(window)

            # Transición progresiva
            tiempo = pygame.time.get_ticks() - self._fin_timestamp
            if tiempo > 1000:  # esperar 1 segundo antes de empezar a oscurecer
                self.fade_alpha = min(255, (tiempo - 1000) // 4)
                self.fade_surface.set_alpha(self.fade_alpha)
                window.blit(self.fade_surface, (0, 0))

            # Cuando el fade llega a negro se sale del combate
            if self.fade_alpha >= 255:
                return self.partida.resultado
            return None

        # ===========================================
        # BLOQUEO TOTAL SI HAY TEXTO EN PANTALLA
        # ===========================================
        if self.estado == "texto":
            self.actualizar_texto_accion()
            self.draw(window)
            return

        # Actualizar texto si no estamos en estado "texto"
        self.actualizar_texto_accion()

        # ============================================================
        # PAUSA DEL COMBATE SI ESTAMOS EN EL MENÚ DE AYUDA
        # ============================================================
        if self.estado == "ayuda":
            self.draw(window)
            return

        # ============================================
        # ESTADOS ESPECIALES (VIDEOS Y TRANSICIONES)
        # ============================================
        if self.estado == "pre_video_fade_in":
            self.fade_in_pre_video(window, dt)
            return

        if self.estado == "video_vs":
            self.reproducir_video_vs(window, dt)
            return

        if self.estado == "post_video_fade_out":
            self.fade_out_post_video(window, dt)
            return

        # ================================
        # SISTEMA NORMAL DEL COMBATE
        # =================================
        self.recalcular_posiciones()
        self.detectar_hover()
        self.actualizar_zoom_card()

        if self.estado == "inicio_turno":
            self.logica_inicio_turno()
        elif self.estado == "seleccion":
            self.logica_seleccion(keys)
        elif self.estado == "confirmar":
            self.logica_confirmar(keys)
        elif self.estado == "rival":
            self.logica_rival()

        # ===========================
        # DIBUJADO FINAL
        # ===========================
        self.draw(window)
        return None

    # =================
    # DIBUJO GENERAL
    # =================
    def draw(self, window):
        window.blit(self.mesa_surface, (0, 0))

        # Texto del turno 
        turno_surface = self.textbox_font.render(self.texto_turno, True, (255, 255, 255))
        turno_x = self.ancho - turno_surface.get_width() - 40
        turno_y = 20
        window.blit(turno_surface, (turno_x, turno_y))

        # Texto de ayuda en la esquina superior derecha
        icono_x = turno_x - self.icono_ayuda.get_width() - 10
        icono_y = turno_y
        window.blit(self.icono_ayuda, (icono_x, icono_y))

        # Actualizar rect para clics
        self.rect_icono_ayuda.topleft = (icono_x, icono_y)
        window.blit(self.img_mazo, self.pos_mazo)
        window.blit(self.oponente_surface, (self.ancho // 2 - 150, 150))

        cantidad_r = min(len(self.cartas_rival), len(self.pos_cartas_rival))
        for i in range(cantidad_r):
            x, y = self.pos_cartas_rival[i]
            window.blit(self.img_reverso, (x, y))

        cantidad_j = min(len(self.cartas_jugador), len(self.pos_cartas_jugador))
        for i in range(cantidad_j):
            carta = self.cartas_jugador[i]
            x, y = self.pos_cartas_jugador[i]

            if carta in self.cartas_elevadas:
                draw_y = y - 20
            else:
                draw_y = y

            window.blit(carta.img_small, (x, draw_y))

            if self.estado == "seleccion" and i == self.carta_seleccionada:
                pygame.draw.rect(window, (255, 255, 0), (x, draw_y, 96, 135), 3)

            if carta in self.cartas_elevadas:
                pygame.draw.rect(window, (0, 150, 255), (x, draw_y, 96, 135), 4)

        if self.ultima_carta:
            window.blit(self.ultima_carta.img_small, (self.ancho - 168, self.alto // 2 - 90))

        self.draw_zoom_card(window)
        self.draw_barras(window)
        self.draw_textbox(window)

        if self.estado == "confirmar" and self.carta_pendiente:
            self.draw_confirmacion(window)

        if self.estado == "ayuda":
            self.draw_ayuda(window)
            return
        
        # ========================================================
        # RECUADRO DE ACCIÓN CON AJUSTE AUTOMÁTICO DE TAMAÑO 
        # ========================================================
        if self.texto_accion_visible and self.texto_accion_alpha > 0:
            lineas = self.texto_accion_visible.split("\n")
            alto_linea = 22

            # Ajuste automático del panel
            panel_w = max(300, max(self.font_accion.size(l)[0] for l in lineas) + 20)
            panel_h = 20 + len(lineas) * alto_linea
            carta_x = self.ancho - 168
            carta_y = self.alto // 2 - 90
            panel_x = carta_x
            panel_y = carta_y + 150

            if panel_x + panel_w > self.ancho - 20:
                panel_x = self.ancho - panel_w - 20
            panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            panel.fill((0, 0, 0, 200))
            pygame.draw.rect(panel, (255, 255, 255), (0, 0, panel_w, panel_h), 3)

            for i, linea in enumerate(lineas):
                texto_surface = self.font_accion.render(linea, True, (255, 255, 0))
                texto_surface.set_alpha(self.texto_accion_alpha)
                panel.blit(texto_surface, (10, 10 + i * alto_linea))
            window.blit(panel, (panel_x, panel_y))

    # ====================
    # MENU DE AYUDA
    # ====================
    def draw_ayuda(self, window):
        # Inicializar scroll si no existe
        if not hasattr(self, "ayuda_scroll"):
            self.ayuda_scroll = 0

        # Fondo semitransparente
        overlay = pygame.Surface(window.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        window.blit(overlay, (0, 0))

        # Panel
        panel_w = 900
        panel_h = 500
        panel_x = (self.ancho - panel_w) // 2
        panel_y = (self.alto - panel_h) // 2
        panel = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(window, (40, 40, 40), panel, border_radius=12)
        pygame.draw.rect(window, (200, 200, 200), panel, 3, border_radius=12)

        # Contenido del panel
        lineas = [
            "COMBINACIONES:",
            "- SET COMPLETO (4 licores distintos): Cubata Legendario (+40-60 borrachera)",
            "- TRÍO (3 iguales): Borrachera Táctica (robas 1, rival pierde 1, +25-30 borrachera)",
            "- PAREJA (2 iguales): Doble Chupito (robas 1, rival pierde 1, +18 borrachera)",
            "",
            "SINERGIAS:",
            "- Vermut + Ataque: +10 borrachera",
            "- Orujo + Ataque Fuerte: +15 borrachera",
            "- Pacharán + Defensa: +10 escudo",
            "- Anís + Evento: +5 borrachera",
            "- 3 licores distintos: +30 borrachera",
            "",
            "TIPOS DE CARTA:",
            "- ATAQUE: aumenta borrachera del rival",
            "- DEFENSA: añade escudo",
            "- ACCIÓN: efectos especiales",
            "- EVENTO: efectos globales o aleatorios",
            "",
            "Pulsa ESC para volver"
        ]

        # Crear superficie interna para scroll
        contenido_w = panel_w - 60
        contenido_h = 1200  # Buen tamaño para el contenido, no tocar más
        contenido = pygame.Surface((contenido_w, contenido_h), pygame.SRCALPHA)

        # Dibujar texto en la superficie interna
        y = 0
        for linea in lineas:
            texto = self.textbox_font.render(linea, True, (255, 255, 255))
            contenido.blit(texto, (0, y))
            y += 32

        # Limitar scroll
        visible_h = panel_h - 80
        min_scroll = -(y - visible_h)
        max_scroll = 0
        self.ayuda_scroll = max(min(self.ayuda_scroll, max_scroll), min_scroll)

        # Área visible del panel
        clip_rect = pygame.Rect(panel_x + 30, panel_y + 40, contenido_w, visible_h)
        window.set_clip(clip_rect)

        # Dibujar contenido desplazado
        window.blit(contenido, (panel_x + 30, panel_y + 40 + self.ayuda_scroll))

        # Quitar clipping
        window.set_clip(None)

