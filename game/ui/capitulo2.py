import pygame
from partida import Partida
import math


class Capitulo2:
    def __init__(self):
        self.partida = Partida(capitulo=2)

        # ====================
        # FONDO DEL ESCENARIO
        # ======================
        self.fondo = pygame.image.load(
            "game/ui/assets/escenarios/capitulo2.png"
        ).convert()

        self.fondo = pygame.transform.scale(
            self.fondo,
            (1280, 720)
        )

        # ========
        # JUGADOR
        # ========
        self.jugador = pygame.Rect(640, 620, 32, 48)
        self.sprite_frente = pygame.image.load("game/ui/assets/personajes/protagonista/frente.png").convert_alpha()
        self.sprite_espalda = pygame.image.load("game/ui/assets/personajes/protagonista/espalda.png").convert_alpha()
        self.sprite_izquierda = pygame.image.load("game/ui/assets/personajes/protagonista/izquierda.png").convert_alpha()
        self.sprite_derecha = pygame.image.load("game/ui/assets/personajes/protagonista/derecha.png").convert_alpha()
        tam = (105, 137)
        self.sprite_frente = pygame.transform.scale(self.sprite_frente,tam)
        self.sprite_espalda = pygame.transform.scale(self.sprite_espalda,tam)
        self.sprite_izquierda = pygame.transform.scale(self.sprite_izquierda,tam)
        self.sprite_derecha = pygame.transform.scale(self.sprite_derecha,tam)
        self.sprite_actual = self.sprite_frente
        self.vel = 4
        self.posicion_pre_combate = None
        # ===============================
        # POSICIONES DE LAS COLISIONES
        # ===========v===================
        self.colisiones = [
            pygame.Rect(20, 20, 630, 320),
            pygame.Rect(30, 510, 400, 180),
            pygame.Rect(710, 20, 520, 650),
        ]

        # ==================
        # GENERAR RIVAL
        # ==================
        self.gallito_rect = pygame.Rect(240, 300, 120, 60)
        self.dialogo_gallito_mostrado = False
        self.iniciar_combate = False
        self.e_pulsado_antes = False

        # ============================
        # ICONO DE DIÁLOGO CON LA E 
        # ============================
        self.icono_e = pygame.image.load(
            "game/ui/assets/objetos/icono_e.png"
        ).convert_alpha()

        self.icono_e = pygame.transform.scale(
            self.icono_e,
            (32, 32)
        )
        self.tiempo = 0

        # ==================================================================
        # INTERACCIÓN CON LA PUERTA Y POR TANTO, INICIAR EL CAPÍTULO 3
        # ==================================================================
        self.salida_rect = pygame.Rect(50, 600, 80, 80)

    # ========================
    # ENTRADA AL CAPÍTULO 2
    # ========================
    def on_enter(self):
        p = self.partida.narrar

        p("NARRADOR: Tras la experiencia en la taberna de Manolo, decides seguir mejorando.")
        p("NARRADOR: Las indicaciones te llevan hasta la famosa Peña del Gallo Rojo.")
        p("NARRADOR: Allí se reúnen algunos de los mejores jugadores de Sevilla.")
        p("NARRADOR: Entre ellos destaca un nombre por encima del resto.")
        p("NARRADOR: Gallito.")
        p("NARRADOR: Algunos lo consideran un genio de las cartas.")
        p("NARRADOR: Otros dicen que aprendió a respetar el juego después de cometer muchos errores con el alcohol.")

    # ========================================================
    # EREUTILIZAR LA POSICION DEL JUGADOR PARA LAS DERROTAS
    # ========================================================
    def reiniciar_tras_derrota(self):

        self.partida = Partida(capitulo=2)

        self.dialogo_gallito_mostrado = False
        self.iniciar_combate = False
        self.e_pulsado_antes = False

        if self.posicion_pre_combate:
            self.jugador.x = self.posicion_pre_combate[0]
            self.jugador.y = self.posicion_pre_combate[1]

    def mostrar_dialogo_derrota(self):

        self.partida.narrar(
            "NARRADOR: Las sirenas de una ambulancia resuenan en tu memoria."
        )

        self.partida.narrar(
            "NARRADOR: Esta vez has aprendido de la forma más dura que el exceso de alcohol tiene consecuencias reales."
        )

        self.partida.narrar(
            "GALLITO: Ya veo que el susto no te ha quitado las ganas de aprender."
        )

        self.partida.narrar(
            "GALLITO: Escucha bien, Alejandro."
        )

        self.partida.narrar(
            "GALLITO: Hay jugadores que creen que aguantar más bebida les hace más fuertes."
        )

        self.partida.narrar(
            "GALLITO: Se equivocan."
        )

        self.partida.narrar(
            "GALLITO: La verdadera fortaleza está en conocer tus límites."
        )

        self.partida.narrar(
            "GALLITO: Controlar lo que haces siempre será más difícil que dejarte llevar."
        )

        self.partida.narrar(
            "GALLITO: Descansa, piensa en lo ocurrido y vuelve cuando estés preparado."
        )

    # =======
    # UPDATE
    # =======
    def update(self, window, keys):
        self.tiempo += 0.1
        window.blit(self.fondo, (0, 0))
        old_pos = self.jugador.copy()

        if keys[pygame.K_w]:
            self.jugador.y -= self.vel
            self.sprite_actual = self.sprite_espalda

        if keys[pygame.K_s]:
            self.jugador.y += self.vel
            self.sprite_actual = self.sprite_frente

        if keys[pygame.K_a]:
            self.jugador.x -= self.vel
            self.sprite_actual = self.sprite_izquierda

        if keys[pygame.K_d]:
            self.jugador.x += self.vel
            self.sprite_actual = self.sprite_derecha

        # Colisiones
        for col in self.colisiones:
            if self.jugador.colliderect(col):
                self.jugador = old_pos
                break

        # Jugador
        sprite_x = (
            self.jugador.centerx
            - self.sprite_actual.get_width() // 2
        )

        sprite_y = (
            self.jugador.bottom
            - self.sprite_actual.get_height()
        )

        window.blit(
            self.sprite_actual,
            (sprite_x, sprite_y)
        )
        pulsando_e = keys[pygame.K_e]
        nueva_pulsacion_e = pulsando_e and not self.e_pulsado_antes

        # ======
        # RIVAL
        # ======
        if self.jugador.colliderect(self.gallito_rect):
            alpha = int((math.sin(self.tiempo * 4) + 1) * 127)
            icono = self.icono_e.copy()
            icono.set_alpha(alpha)

            window.blit(
                icono,
                (
                    self.gallito_rect.x + 20,
                    self.gallito_rect.y - 40
                )
            )

            if nueva_pulsacion_e and not self.dialogo_gallito_mostrado:
                self.dialogo_gallito_mostrado = True
                self.iniciar_combate = True
                self.partida.narrar(
                    "GALLITO: Así que tú eres Alejandro."
                )

                self.partida.narrar(
                    "GALLITO: He escuchado lo que ocurrió en la taberna."
                )

                self.partida.narrar(
                    "JUGADOR: Ya veo que las noticias vuelan."
                )

                self.partida.narrar(
                    "GALLITO: Aquí todos hablan. Lo importante es aprender de lo que pasó."
                )

                self.partida.narrar(
                    "GALLITO: Muchos creen que ser fuerte consiste en aguantar más alcohol."
                )

                self.partida.narrar(
                    "GALLITO: Yo aprendí hace años que la verdadera habilidad está en saber cuándo parar."
                )

                self.partida.narrar(
                    "JUGADOR: Entonces... ¿vas a enseñarme?"
                )

                self.partida.narrar(
                    "GALLITO: Primero voy a comprobar si estás preparado para escuchar."
                )

                self.partida.narrar(
                    "GALLITO: Siéntate. Juguemos una partida."
                )

        # ==================================================
        # COMBATE AUTOMÁTICO TRAS EL DIÁLOGO CON EL RIVAL
        # ==================================================
        if self.iniciar_combate:
            dialogo = self.partida.ui.dialogue
            if not dialogo.visible and len(dialogo.queue) == 0:
                self.posicion_pre_combate = (
                    self.jugador.x,
                    self.jugador.y
                )
                self.iniciar_combate = False
                return "combate"

        # ================================================================
        # INTERACCIÓN CON LA PUERTA Y POR TANTO, INICIAR EL CAPÍTULO 2
        # ================================================================
        if self.jugador.colliderect(self.salida_rect):
            alpha = int((math.sin(self.tiempo * 4) + 1) * 127)
            icono = self.icono_e.copy()
            icono.set_alpha(alpha)

            window.blit(
                icono,
                (
                    self.salida_rect.x + 20,
                    self.salida_rect.y - 40
                )
            )

            if nueva_pulsacion_e:
                self.partida.narrar(
                    "NARRADOR: Sales de la Peña del Gallo Rojo."
                )
                return "capitulo3"
        self.e_pulsado_antes = pulsando_e
        return None