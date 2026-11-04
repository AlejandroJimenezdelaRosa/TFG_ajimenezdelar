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
        self.jugador = pygame.Rect(664, 572, 32, 48)
        self.vel = 4

        # ===============================
        # POSICIONES DE LAS COLISIONES
        # ===========v===================
        self.colisiones = [
            pygame.Rect(210, 400, 200, 80),
            pygame.Rect(210, 556, 200, 80),
            pygame.Rect(20, 284, 80, 368),
            pygame.Rect(20, 220, 552, 80),
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

        p("NARRADOR: Llegas a la Peña del Gallo Rojo.")
        p("NARRADOR: El ambiente está cargado de música, risas y humo.")
        p("NARRADOR: Todos hablan de un tal Gallito.")
        p("NARRADOR: Dicen que es el mejor jugador de toda Sevilla.")

    # =======
    # UPDATE
    # =======
    def update(self, window, keys):
        self.tiempo += 0.1
        window.blit(self.fondo, (0, 0))
        old_pos = self.jugador.copy()

        if keys[pygame.K_w]:
            self.jugador.y -= self.vel
        if keys[pygame.K_s]:
            self.jugador.y += self.vel
        if keys[pygame.K_a]:
            self.jugador.x -= self.vel
        if keys[pygame.K_d]:
            self.jugador.x += self.vel

        # Colisiones
        for col in self.colisiones:
            if self.jugador.colliderect(col):
                self.jugador = old_pos
                break

        # Jugador
        pygame.draw.rect(window, (255, 255, 0), self.jugador)
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
                    "GALLITO: Hombre... ya era hora de que aparecieras."
                )

                self.partida.narrar(
                    "GALLITO: Así que tú eres Alejandro."
                )

                self.partida.narrar(
                    "GALLITO: Llevo días escuchando historias sobre ti."
                )

                self.partida.narrar(
                    "JUGADOR: Espero que sean buenas."
                )

                self.partida.narrar(
                    "GALLITO: Eso vamos a averiguar ahora."
                )

                self.partida.narrar(
                    "GALLITO: En esta peña las palabras no tienen valor."
                )

                self.partida.narrar(
                    "GALLITO: Aquí se habla jugando."
                )

                self.partida.narrar(
                    "GALLITO: Ven. Siéntate. Es hora de probar tu talento."
                )

        # ==================================================
        # COMBATE AUTOMÁTICO TRAS EL DIÁLOGO CON EL RIVAL
        # ==================================================
        if self.iniciar_combate:
            dialogo = self.partida.ui.dialogue
            if not dialogo.visible and len(dialogo.queue) == 0:
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