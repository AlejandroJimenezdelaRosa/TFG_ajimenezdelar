import pygame
from partida import Partida
import math

class Capitulo1:
    def __init__(self):
        # ===================
        # FONDO DEL CAPÍTULO
        # ===================
        self.fondo = pygame.image.load(
            "game/ui/assets/escenarios/capitulo1.png"
        ).convert()

        self.fondo = pygame.transform.scale(
            self.fondo,
            (1280, 720)
        )

        self.trigger_mesa4 = pygame.Rect(800,400,105,80)

        # ========
        # PARTIDA
        # ========
        self.partida = Partida(capitulo=1)
        self.up_pulsado = False
        self.down_pulsado = False
        self.enter_pulsado = False
        self.esperando_dialogo_decision = False

        # ========================
        # ESTADOS DE LA NARRACIÓN
        # ========================
        self.esperando_mesa4 = False
        self.mesa4_activada = False
        self.opciones_tutorial_activas = False
        self.opciones_post_combate_activas = False
        self.opciones_fin_tutorial_activas = False

        # Menú del tutorial
        self.mostrando_opciones_tutorial = False
        self.opcion_seleccionada = 0

        # Menú final del tutorial
        self.mostrando_opciones_fin_tutorial = False
        self.opcion_fin_tutorial = 0

        # ========
        # JUGADOR
        # ========
        self.jugador = pygame.Rect(624, 336, 32, 48)
        self.vel = 4
        self.post_combate = False

        # ============================
        # POSICIONES DE LAS COLISIONES
        # ============================
        self.colisiones = [
            # Cocina + barra
            pygame.Rect(21,0,449,380),

            # Barra y zona de servicio
            pygame.Rect( 474,0,786,307),

            # Superior izquierda
            pygame.Rect(70, 425, 110, 70),

            # Superior centro izquierda
            pygame.Rect(265, 425, 110, 70),

            # Superior derecha
            pygame.Rect(1025, 425, 110, 70),

            # Inferior izquierda
            pygame.Rect(80, 560, 110, 70),

            # Inferior centro izquierda
            pygame.Rect(285, 560, 110, 70),

            # Inferior derecha
            pygame.Rect(1025, 560, 110, 70),

            pygame.Rect(1170,575,50,80),

            # Mesa inferior central
            pygame.Rect(800,570,110,70),
        ]
        
        # Icono del diálogo con la E 
        self.icono_e = pygame.image.load("game/ui/assets/objetos/icono_e.png").convert_alpha()
        self.icono_e = pygame.transform.scale(self.icono_e, (32, 32))

        # Tiempo para animación del icono 
        self.tiempo = 0

        # Puerta de salida (Iniciar siguiente cap)
        self.puerta_rect = pygame.Rect(1100, 600, 80, 80)

    # ============================================================
    # ENTRADA AL CAPÍTULO 1
    # ============================================================
    def on_enter(self):
        self.mostrar_intro_capitulo1()

    # ============================================================
    # NARRATIVA INICIAL
    # ============================================================
    def mostrar_intro_capitulo1(self):
        self.partida.narrar("MANOLO: ¡Alejandro! La mesa 4 está hecha un desastre.")
        self.partida.narrar("MANOLO: Anda, límpiala antes de que se me quejen.")

        self.partida.narrar("CONTROLES:")
        self.partida.narrar("Muévete con W A S D.")
        self.partida.narrar("Pulsa E para interactuar.")
        self.partida.narrar("Pulsa ESPACIO o CLICK para continuar los diálogos.")
        self.partida.narrar("Cuando aparezcan opciones, selecciónalas con ↑ ↓ y confirma con ENTER.")

        self.esperando_mesa4 = True

    # ============================================================
    # MESA 4 y TUTORIAL
    # ============================================================
    def narrativa_mesa4(self):
        self.partida.narrar("Te acercas a la mesa 4…")
        self.partida.narrar("Cuatro desconocidos te miran con una sonrisa sospechosa.")
        self.partida.narrar("BIGOTES: Quillo, ¿tú sabes jugar a esto?")
        self.partida.narrar("PROTAGONISTA: ¿A qué?")
        self.partida.narrar("INFORMÁTICO: A esto, criatura. El juego de cartas más famoso del barrio.")
        self.partida.narrar("POETA: Siéntate, que te enseñamos.")
        self.partida.narrar("Comienza el tutorial improvisado…")

        self.esperando_mesa4 = False
        self.mesa4_activada = True
        self.opciones_tutorial_activas = True

        self.partida.ui.dialogue.text = (
            "BIGOTES: ¿Quieres que te expliquemos cómo jugar?"
        )

        self.partida.ui.dialogue.set_options([
            "Explicación de cómo se juega",
            "Saltar tutorial"
        ])

    # ============================================================
    # TUTORIAL COMPLETO
    # ============================================================
    def iniciar_tutorial(self):
        self.mostrando_opciones_tutorial = False

        self.partida.narrar("El objetivo es emborrachar al rival antes de que él te emborrache a ti.")
        self.partida.narrar("Cada ataque sube la borrachera del rival.")
        self.partida.narrar("[Pulsa CLICK o ESPACIO para continuar]")

        self.partida.narrar("TIPOS DE CARTAS")
        self.partida.narrar("• ATAQUE → suben borrachera al rival")
        self.partida.narrar("• DEFENSA / CURACIÓN → bajan tu borrachera")
        self.partida.narrar("• ACCIÓN → efectos especiales (robar, esquivar, etc.)")
        self.partida.narrar("• SET → si juntas 3 iguales, activas un COMBO")
        self.partida.narrar("[Pulsa CLICK o ESPACIO para continuar]")

        self.partida.narrar("ESTADOS")
        self.partida.narrar("• Sobrio (0–40%) → normal")
        self.partida.narrar("• Contentillo (40–70%) → +daño, -precisión")
        self.partida.narrar("• Tocado (70–90%) → +daño recibido, -precisión")
        self.partida.narrar("• Ciego (90–100%) → ataques torpes, riesgo de autoataque")
        self.partida.narrar("[Pulsa CLICK o ESPACIO para continuar]")

        self.partida.narrar("PRECISIÓN Y CRÍTICOS")
        self.partida.narrar("Tus ataques pueden fallar según tu estado.")
        self.partida.narrar("También pueden ser críticos y hacer más daño.")
        self.partida.narrar("[Pulsa CLICK o ESPACIO para continuar]")

        self.partida.narrar("COMBOS")
        self.partida.narrar("Si juntas 3 cartas de set iguales, puedes activar un combo muy potente.")
        self.partida.narrar("[Fin del tutorial — pulsa CLICK o ESPACIO]")

    # ============================================================
    # DISTANCIA
    # ============================================================
    def distancia(self, r1, r2):
        cx1 = r1.x + r1.w // 2
        cy1 = r1.y + r1.h // 2
        cx2 = r2.x + r2.w // 2
        cy2 = r2.y + r2.h // 2
        return ((cx1 - cx2)**2 + (cy1 - cy2)**2) ** 0.5

    # ============================================================
    # UPDATE PRINCIPAL
    # ============================================================
    def update(self, window, keys):
        self.tiempo += 0.1

        # Fondo
        window.blit(self.fondo, (0, 0))

        # Dibujar puerta
        # window.blit(self.puerta_img, self.puerta_rect)

        # Movimiento del jugador (solo si no hay menús)
        old_pos = self.jugador.copy()
        if not self.mostrando_opciones_tutorial and not self.mostrando_opciones_fin_tutorial:
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

        # Dibujar jugador
        pygame.draw.rect(window, (255, 255, 0), self.jugador)

        # ============================================================
        # INTERACCIÓN CON LA MESA 4
        # ============================================================
        if self.esperando_mesa4 and not self.mesa4_activada:
            brillo = pygame.Surface((self.trigger_mesa4.w, self.trigger_mesa4.h), pygame.SRCALPHA)
            brillo.fill((255, 255, 0, 80))
            window.blit(brillo, (self.trigger_mesa4.x, self.trigger_mesa4.y))

            if self.distancia(self.jugador, self.trigger_mesa4) < 70:
                alpha = int((math.sin(self.tiempo * 4) + 1) * 127)
                icono = self.icono_e.copy()
                icono.set_alpha(alpha)
                window.blit(icono, (self.trigger_mesa4.x + 20, self.trigger_mesa4.y - 40))

                if keys[pygame.K_e]:
                    self.narrativa_mesa4()

        # ============================================================
        # ACTIVAR MENÚ FINAL DEL TUTORIAL CUANDO EL DIÁLOGO TERMINE
        # ============================================================
        dialogo = self.partida.ui.dialogue

        if dialogo.showing_options:
            if keys[pygame.K_RETURN]:
                opcion = dialogo.confirm_option()

                if opcion is not None:
                    # Tutorial
                    if self.opciones_tutorial_activas:
                        self.opciones_tutorial_activas = False
                        if opcion == 0:
                            self.iniciar_tutorial()
                            
                        elif opcion == 1:
                            self.partida.narrar(
                                "BIGOTES: Vale, vale... directo al lío entonces."
                            )

                            self.partida.narrar(
                                "Que empiece la partida."
                            )
                            return "combate"

                    elif self.opciones_fin_tutorial_activas:
                        self.opciones_fin_tutorial_activas = False

                        if opcion == 0:

                            self.iniciar_tutorial()

                        elif opcion == 1:
                            self.partida.narrar(
                                "BIGOTES: Pues venga, al lío."
                            )

                            self.partida.narrar(
                                "Que empiece la partida."
                            )
                            return "combate"

                    elif self.opciones_post_combate_activas:
                        self.opciones_post_combate_activas = False

                        if opcion == 0:
                            self.partida.decision_cap1 = "celebrar"
                            self.partida.narrar(
                                "NARRADOR: Decides quedarte celebrando hasta altas horas."
                            )

                            self.partida.narrar(
                                "MANOLO: ¡Jajaja! Ya sabía yo que te ibas a quedar."
                            )

                            self.partida.narrar(
                                "MANOLO: Una noche de fiesta está bien."
                            )

                            self.partida.narrar(
                                "MANOLO: El problema es cuando todas las noches son iguales."
                            )

                        elif opcion == 1:
                            self.partida.decision_cap1 = "moderado"

                            self.partida.narrar(
                                "NARRADOR: Tomas algo con los demás antes de marcharte."
                            )

                            self.partida.narrar(
                                "MANOLO: Buena elección."
                            )

                            self.partida.narrar(
                                "MANOLO: Hay tiempo para celebrar y tiempo para descansar."
                            )

                        elif opcion == 2:
                            self.partida.decision_cap1 = "descansar"

                            self.partida.narrar(
                                "NARRADOR: Prefieres volver a casa y descansar."
                            )

                            self.partida.narrar(
                                "MANOLO: Veo que piensas a largo plazo."
                            )

                            self.partida.narrar(
                                "MANOLO: Descansar también forma parte del entrenamiento."
                            )
                        self.esperando_dialogo_decision = True

        if self.mesa4_activada and not dialogo.showing_options:
            if not dialogo.visible and len(dialogo.queue) == 0:
                self.mesa4_activada = False
                dialogo.visible = True
                dialogo.text = (
                    "BIGOTES: ¿Quieres repasar el tutorial o empezamos el combate?"
                )

                dialogo.set_options([
                    "Repetir tutorial",
                    "Empezar combate"
                ])
                self.opciones_fin_tutorial_activas = True

        # ============================================================
        # ESPERAR A QUE TERMINEN LOS DIÁLOGOS DE LA DECISIÓN
        # ============================================================
        if self.esperando_dialogo_decision:
            if not dialogo.visible and len(dialogo.queue) == 0:
                self.esperando_dialogo_decision = False
                self.escena_manolo()

        # ============================================================
        # POST-COMBATE Y ESPERAR A QUE ACABEN LOS DIÁLOGOS
        # ============================================================
        if self.post_combate:
            if not dialogo.visible and len(dialogo.queue) == 0:
                print("POST COMBATE")
                self.post_combate = False

                self.opciones_post_combate_activas = True
                print("MOSTRANDO OPCIONES COMBATE")

                self.partida.ui.dialogue.visible = True
                self.partida.ui.dialogue.text = (
                    "MANOLO: ¿Cómo quieres celebrar la victoria?"
                )

                self.partida.ui.dialogue.set_options([
                    "Quedarme hasta tarde celebrando",
                    "Tomar algo y volver a casa",
                    "Irme directamente a descansar"
                ])

        # ============================================================
        # INTERACCIÓN CON LA PUERTA Y POR TANTO, INICIAR EL CAPÍTULO 2
        # ============================================================
        if not self.post_combate:
            if self.distancia(self.jugador, self.puerta_rect) < 70:
                alpha = int((math.sin(self.tiempo * 4) + 1) * 127)
                icono = self.icono_e.copy()
                icono.set_alpha(alpha)
                window.blit(icono, (self.puerta_rect.x + 20, self.puerta_rect.y - 40))

                if keys[pygame.K_e]:
                    self.partida.narrar("NARRADOR: Sales de la taberna mientras la noche sevillana te envuelve.")
                    self.partida.narrar("NARRADOR: El eco de las risas, las cartas y los brindis queda atrás…")
                    self.partida.narrar("NARRADOR: …y sin saberlo, das el primer paso hacia una aventura mucho más grande.")
                    self.partida.narrar("NARRADOR: FIN DEL CAPÍTULO 1.")
                    return "capitulo2"
        return None

    # ============================================================
    # FIN DEL COMBATE
    # ============================================================
    def on_fin_combate(self, resultado):

        if resultado == "victoria":
            self.partida.narrar("BIGOTES: ¡Ole ahí! Les has dado una paliza, criatura.")
            self.partida.narrar("POETA: Niño, tienes talento. El arte te corre por las venas.")
            self.partida.narrar("INFORMÁTICO: Te has ganado una ronda gratis… y mi respeto, que es más difícil.")
            self.partida.narrar("BIGOTES: Escúchame, Alejandro… no todo el mundo aprende tan rápido.")
            self.partida.narrar("POETA: El duende del cartón te acompaña, muchacho.")
            self.partida.narrar("INFORMÁTICO: Y hablando de duendes… ¿has oído hablar del 'Gallito'?")
            self.partida.narrar("BIGOTES: Ese tío es una leyenda. Juega en la Peña del Gallo Rojo, ahí al lado del puente.")
            self.partida.narrar("POETA: Dicen que nunca ha perdido un duelo… o que cuando pierde, nadie vive pa’ contarlo.")
            self.partida.narrar("INFORMÁTICO: Si quieres mejorar, deberías ir a verlo. Igual te enseña algo… o te revienta.")
            self.partida.narrar("BIGOTES: Pero no hoy. Hoy disfruta. Que lo que viene es gordo.")
            self.partida.narrar("MANOLO: ¡Alejandro! Cuando termines con estos, acércate a la barra. Tengo que pedirte un favor importante.")
            self.partida.narrar("NARRADOR: Algo se mueve en Sevilla… y tú estás en medio sin saberlo.")

        else:
            self.partida.narrar("BIGOTES: Ay, criatura… te han dado pa'l pelo.")
            self.partida.narrar("POETA: No pasa ná, el arte también es perder.")
            self.partida.narrar("INFORMÁTICO: Venga, siéntate y descansa un poco.")
            self.partida.narrar("BIGOTES: Mira, Alejandro… perder es parte del camino. Aquí nadie nació sabiendo.")
            self.partida.narrar("POETA: El fracaso es un maestro severo, pero justo.")
            self.partida.narrar("INFORMÁTICO: Si quieres mejorar, deberías visitar la Peña del Gallo Rojo.")
            self.partida.narrar("BIGOTES: Allí está el 'Gallito'. Ese sí que sabe. Te puede enseñar un par de trucos.")
            self.partida.narrar("POETA: Pero no ahora. Ahora respira, que casi te caes redondo.")
            self.partida.narrar("MANOLO: ¡Alejandro! Cuando puedas, acércate a la barra. Tengo que hablar contigo.")
            self.partida.narrar("NARRADOR: Quizá esta derrota sea el primer paso hacia algo más grande…")

        self.post_combate = True
        self.mesa4_activada = False

    # ============================================================
    # DIÁLOGOS DE MANOLO COMO MENTOR
    # ============================================================
    def escena_manolo(self):
        p = self.partida.narrar

        p("MANOLO: Ven pa'cá, Alejandro. Siéntate un momento conmigo.")
        p("MANOLO: Mira, hijo… hoy has vivido tu primer duelo de verdad.")
        p("MANOLO: Y te voy a decir una cosa: aquí en Sevilla, el juego de cartas no es solo un pasatiempo.")
        p("MANOLO: Es orgullo. Es tradición. Es… bueno, también es una excusa pa' beber, pero tú me entiendes.")

        p("MANOLO: Los del barrio ya han empezado a hablar de ti.")
        p("MANOLO: Que si el chaval nuevo tiene arte… que si apunta maneras… que si tiene más peligro que un cubata mal hecho.")
        p("MANOLO: Y eso, Alejandro, es bueno. Muy bueno.")

        p("MANOLO: Pero escucha… también significa que te van a empezar a buscar.")
        p("MANOLO: Retadores. Gente que quiere medirse contigo. Gente que quiere demostrar que son mejores.")
        p("MANOLO: Y tú tienes que estar preparado.")

        p("MANOLO: Mañana, pásate por la Peña del Gallo Rojo.")
        p("MANOLO: Allí se junta gente seria. Jugadores de verdad.")
        p("MANOLO: Y si quieres seguir creciendo… ese es tu sitio.")

        p("MANOLO: Pero por hoy ya está bien. Estás cansado, y se te nota en la cara.")
        p("MANOLO: Vete pa' casa, descansa, y mañana empieza lo bueno.")

