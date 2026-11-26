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
        self.mostrar_dialogo_consecuencias = False
        self.post_combate = False
        self.opciones_post_combate_activas = False
        self.esperando_dialogo_decision = False
        self.combate_ganado = False

        # ===============================
        # POSICIONES DE LAS COLISIONES
        # ===========v===================
        self.colisiones = [
            pygame.Rect(20, 20, 680, 320),
            pygame.Rect(30, 510, 400, 180),
            pygame.Rect(710, 20, 520, 650),
            # Paredes
            pygame.Rect(0, 0, 30, 720),
            pygame.Rect(1250, 0, 30, 720),
            pygame.Rect(0, 690, 1280, 30),
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

    # ============================================================
    # FIN DEL COMBATE EN CAPÍTULO 2
    # ============================================================
    def on_fin_combate(self, resultado):
        if resultado == "victoria":
            self.combate_ganado = True
            self.partida.narrar("GALLITO: Has jugado con cabeza, Alejandro. No te has pasado de la raya.")
            self.partida.narrar("GALLITO: Ganar no es aguantar más copas; es saber cuándo decir basta.")
            self.partida.narrar("NARRADOR: Has superado el duelo manteniendo el control.")
        else:
            self.partida.narrar("GALLITO: El alcohol te ha nublado la vista antes de tiempo.")
            self.partida.narrar("GALLITO: Cuando pierdes el control, pierdes la partida… y algo más importante.")
            self.partida.narrar("NARRADOR: La resaca y el exceso dejan una lección clara.")

        self.post_combate = True


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

    # ==================================================
    # REINICIAR EL COMBATE PARA EVITAR PROBLEMAS
    # ==================================================
    def preparar_combate_gallito(self):
        decision_cap1 = self.partida.decision_cap1
        ui = self.partida.ui
        self.partida = Partida(capitulo=2)
        self.partida.decision_cap1 = decision_cap1
        self.partida.ui = ui
        return decision_cap1

    def aplicar_penalizacion_capitulo1(self, decision):
        if decision == "celebrar":
            self.partida.jugador.borracha = 35
        
        elif decision == "moderado":
            self.partida.jugador.borracha = 20

        elif decision == "descansar":
            self.partida.jugador.borracha = 0

    # ======================================================================
    # DIALOGOS DE CONSECUENCIAS DEL CAPÍTULO 1 SEGÚN LA DECISIÓN TOMADA
    # ======================================================================
    def mostrar_consecuencias_capitulo1(self):

        decision = self.partida.decision_cap1

        if decision == "celebrar":
            self.partida.narrar("NARRADOR: La larga celebración de anoche todavía pasa factura.")
            self.partida.narrar("NARRADOR: Te cuesta concentrarte y comienzas el duelo con secuelas de la noche anterior.")

        elif decision == "moderado":
            self.partida.narrar("NARRADOR: Descansaste algo, aunque todavía notas algunos efectos de la noche anterior.")
            self.partida.narrar("NARRADOR: No llegas en plenas condiciones, pero tampoco estás en tu peor momento.")

        elif decision == "descansar":
            self.partida.narrar("NARRADOR: Haber descansado y evitado el exceso te permite afrontar el desafío en las mejores condiciones.")
            self.partida.narrar("NARRADOR: Te sientes despejado y preparado para enfrentarte a Gallito.")


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

            if nueva_pulsacion_e and not self.dialogo_gallito_mostrado and not self.combate_ganado:
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
                self.posicion_pre_combate = (self.jugador.x,self.jugador.y)
                decision = self.preparar_combate_gallito()
                self.aplicar_penalizacion_capitulo1(decision)
                self.mostrar_consecuencias_capitulo1()
                self.iniciar_combate = False
                self.mostrar_dialogo_consecuencias = True

        if self.mostrar_dialogo_consecuencias:
            dialogo = self.partida.ui.dialogue
            if not dialogo.visible and len(dialogo.queue) == 0:
                 self.mostrar_dialogo_consecuencias = False
                 return "combate"

        dialogo = self.partida.ui.dialogue

        if dialogo.showing_options:
            if keys[pygame.K_RETURN]:
                opcion = dialogo.confirm_option()

                if opcion is not None and self.opciones_post_combate_activas:
                    self.opciones_post_combate_activas = False

                    if opcion == 0:
                        self.partida.narrar(
                            "GALLITO: Seguir bebiendo para 'celebrar' o 'desahogarte' suele salir caro."
                        )
                        self.partida.narrar(
                            "NARRADOR: Forzar más alcohol solo aumenta los riesgos y la pérdida de control."
                        )
                    elif opcion == 1:
                        self.partida.narrar(
                            "GALLITO: Beber despacio, alternar con agua y poner un límite marca la diferencia."
                        )
                        self.partida.narrar(
                            "NARRADOR: Cuidarte en el momento evita consecuencias mayores después."
                        )
                    elif opcion == 2:
                        self.partida.narrar(
                            "GALLITO: Saber parar a tiempo también es una decisión inteligente."
                        )
                        self.partida.narrar(
                            "NARRADOR: Escuchar a tu cuerpo te permite seguir con claridad."
                        )

                    self.esperando_dialogo_decision = True

        # ============================================================
        # POST-COMBATE Y ESPERAR A QUE ACABEN LOS DIALOGOS
        # ============================================================
        if self.post_combate:
            if not dialogo.visible and len(dialogo.queue) == 0:
                self.post_combate = False
                self.opciones_post_combate_activas = True

                dialogo.visible = True
                dialogo.text = (
                    "GALLITO: Después de un duelo así, ¿qué actitud tomas frente al alcohol?"
                )
                dialogo.set_options([
                    "Seguir bebiendo sin poner límite",
                    "Beber con moderación y alternar con agua",
                    "Parar y evitar seguir sumando alcohol"
                ])

        if self.esperando_dialogo_decision:
            if not dialogo.visible and len(dialogo.queue) == 0:
                self.esperando_dialogo_decision = False
        
        # ================================================================
        # INTERACCIÓN CON LA PUERTA Y POR TANTO, INICIAR EL CAPÍTULO 3
        # ================================================================
        if not self.post_combate and not self.opciones_post_combate_activas and not self.esperando_dialogo_decision:
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

