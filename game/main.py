import pygame
from ui.menu_inicio import MenuInicio
from ui.video_player import VideoPlayer
from ui.capitulo1 import Capitulo1
from ui.capitulo2 import Capitulo2
from ui.ui_manager import UIManager
from ui.escena_combate import EscenaCombate
from ui.minijuego_cervezas import MinijuegoCervezas

pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Escenas
menu = MenuInicio(window)
video = VideoPlayer("game/ui/assets/videos/intro.mp4", (1280, 720))
capitulo1 = Capitulo1()
capitulo2 = None

combate = None
minijuego = None
ui = None

estado = "menu"
fade_alpha = 0
fade_surface = pygame.Surface((1280, 720))
fade_surface.fill((0, 0, 0))

resultado_final = None  # ← para guardar victoria/derrota

espera_intro = 0
alpha_video = 0

fade_video = pygame.Surface((1280, 720))
fade_video.fill((0, 0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ============================================================
        # BLOQUEO TOTAL DE EVENTOS SI ESTAMOS EN EL MENÚ DE AYUDA
        # ============================================================
        if estado == "combate" and combate and combate.estado == "ayuda":

            # Cerrar menú haciendo clic en el icono
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if combate.rect_icono_ayuda.collidepoint(event.pos):
                    combate.estado = "seleccion"
                    continue

            # Scroll del menú
            if event.type == pygame.MOUSEWHEEL:
                combate.ayuda_scroll += event.y * 30
                continue

            continue

        # ============================================================
        # MANEJO NORMAL DE EVENTOS
        # ============================================================

        if estado == "menu":
            opcion = menu.handle_event(event)
            if opcion == "Nueva Partida":
                estado = "transicion_video"
                fade_alpha = 0

                espera_intro = 0
                alpha_fin_video = 0

                video = VideoPlayer(
                    "game/ui/assets/videos/intro.mp4",
                    (1280, 720)
                )
                
        elif estado == "capitulo1":
            if ui:
                ui.handle_event(event)

        elif estado == "capitulo2":
            if ui:
                ui.handle_event(event)

        elif estado == "combate":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if combate.rect_icono_ayuda.collidepoint(event.pos):
                    combate.estado = "ayuda"
                    continue

        elif estado == "minijuego_cervezas":
            pass

    # ================================
    # DIBUJO Y UPDATE DE ESCENAS
    # ===============================

    if estado == "menu":
        menu.draw()

    elif estado == "transicion_video":
        menu.draw()
        fade_alpha += 5
        fade_surface.set_alpha(fade_alpha)
        window.blit(fade_surface, (0, 0))
        if fade_alpha >= 255:
            estado = "video_intro"

    elif estado == "video_intro":
        video.draw(window)
        if video.finished:
            # Fundido progresivo a negro
            if alpha_video < 255:
                alpha_video += 3
            fade_video.set_alpha(alpha_video)
            window.blit(fade_video, (0, 0))

            # Esperar 3 segundos cuando la pantalla ya esté negra
            if alpha_video >= 255:
                espera_intro += clock.get_time()
                if espera_intro >= 3000:
                    ui = UIManager(window, capitulo1.partida)
                    capitulo1.partida.ui = ui
                    capitulo1.on_enter()
                    estado = "capitulo1"

    # ====================
    # CAPÍTULO 1
    # ====================
    elif estado == "capitulo1":
        keys = pygame.key.get_pressed()
        siguiente_estado = capitulo1.update(window, keys)

        if ui:
            ui.draw()

        if siguiente_estado == "combate":
            combate = EscenaCombate(capitulo1.partida)
            estado = "combate"

        elif siguiente_estado == "capitulo2":
            capitulo2 = Capitulo2()
            capitulo2.partida = capitulo1.partida 
            ui = UIManager(window, capitulo2.partida)
            capitulo2.partida.ui = ui
            capitulo2.on_enter()
            estado = "capitulo2"

    # ====================================
    # CAPÍTULO 2
    # ====================================
    elif estado == "capitulo2":
        keys = pygame.key.get_pressed()
        siguiente_estado = capitulo2.update(window, keys)

        if ui:
            ui.draw()

        # Combate
        if siguiente_estado == "combate":
            combate = EscenaCombate(capitulo2.partida)
            estado = "combate"

        # Minijuego de cervezas si se añade
        elif siguiente_estado == "minijuego_cervezas":
            minijuego = MinijuegoCervezas(capitulo2.partida)
            estado = "minijuego_cervezas"

        # Capítulo 3 (cuando exista)
        elif siguiente_estado == "capitulo3":
            pass

    # =====================================
    # MINIJUEGO CERVEZAS (Si se añade)
    # ======================================
    elif estado == "minijuego_cervezas":
        keys = pygame.key.get_pressed()
        resultado = minijuego.update(window, keys)

        if resultado == "fin_minijuego":
            if minijuego.resultado == "exito":
                capitulo2.partida.narrar("GALLITO: Bueno… no está mal. Tienes buen pulso.")
                capitulo2.partida.narrar("GALLITO: Vale, ahora sí podemos hablar.")
            else:
                capitulo2.partida.narrar("GALLITO: ¡Jajaja! Te has pasado. Vuelve cuando aprendas a llenar una jarra.")

            estado = "capitulo2"

    # =================
    # COMBATE
    # =================
    elif estado == "combate":
        keys = pygame.key.get_pressed()
        resultado = combate.update(window, keys)

        # FIN DEL COMBATE CON TRANSICIÓN NEGRA
        if resultado in ("victoria", "derrota"):
            resultado_final = resultado
            estado = "transicion_fin_combate"
            fade_alpha = 0
            fade_surface.set_alpha(0)
            continue

    # ===========================================
    # TRANSICIÓN NEGRA AL SALIR DEL COMBATE
    # ===========================================
    elif estado == "transicion_fin_combate":
        combate.draw(window)

        fade_alpha += 10
        if fade_alpha > 255:
            fade_alpha = 255

        fade_surface.set_alpha(fade_alpha)
        window.blit(fade_surface, (0, 0))

        # Cuando está completamente negro se vuelve al capítulo correcto
        if fade_alpha >= 255:

            # Si el combate pertenece al capítulo 1
            if combate.partida.capitulo == 1:
                capitulo1 = Capitulo1()
                capitulo1.partida = combate.partida

                ui = UIManager(window, capitulo1.partida)
                capitulo1.partida.ui = ui

                capitulo1.on_fin_combate(resultado_final)
                estado = "capitulo1"

            # Si el combate pertenece al capítulo 2
            elif combate.partida.capitulo == 2:
                capitulo2 = Capitulo2()
                capitulo2.partida = combate.partida

                ui = UIManager(window, capitulo2.partida)
                capitulo2.partida.ui = ui

                estado = "capitulo2"

    pygame.display.update()
    clock.tick(60)
