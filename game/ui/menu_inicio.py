import pygame
from save_manager import hay_partida_guardada
import random

class MenuInicio:
    def __init__(self, window):
        self.window = window
        self.width = window.get_width()
        self.height = window.get_height()

        # Fondo
        try:
            self.fondo = pygame.image.load("game/ui/assets/fondo_menu.png").convert()
            self.fondo = pygame.transform.scale(self.fondo, (self.width, self.height))
        except Exception:
            self.fondo = None

        # Botellas diferentes para cada opción del menú porque queda bien
        self.botellas = {}

        def cargar_botellas(nombre, archivo):
            try:
                self.botellas[nombre] = pygame.image.load(archivo).convert_alpha()
            except Exception:
                self.botellas[nombre] = None

        cargar_botellas("Continuar", "game/ui/assets/botella_continuar.png")
        cargar_botellas("Nueva Partida", "game/ui/assets/botella_nueva.png")
        cargar_botellas("Opciones", "game/ui/assets/botella_opciones.png")
        cargar_botellas("Salir", "game/ui/assets/botella_salir.png")

        # Sonido
        try:
            self.sonido_burbujas = pygame.mixer.Sound("game/ui/assets/burbujas.wav")
        except Exception:
            self.sonido_burbujas = None

        # Fuentes
        self.font_title = pygame.font.SysFont("arial", 64)
        self.font_button = pygame.font.SysFont("arial", 40)

        # Botones mças el estado de llenado
        self.buttons = []
        self.estado_llenado = {}
        y = 260

        if hay_partida_guardada():
            rect = pygame.Rect(self.width//2 - 50, y, 300, 80)
            self.buttons.append(("Continuar", rect))
            self.estado_llenado["Continuar"] = 0
            y += 100

        for nombre in ["Nueva Partida", "Opciones", "Salir"]:
            rect = pygame.Rect(self.width//2 - 50, y, 300, 80)
            self.buttons.append((nombre, rect))
            self.estado_llenado[nombre] = 0
            y += 100

        # Transición de fade-in
        self.fade_alpha = 255

    # =============================
    # EFECTO DE LOS LÍQUIDOS 
    # =============================
    def render_text_liquido(self, text, hover=False):
        mask = self.font_button.render(text, True, (255, 255, 255))
        w, h = mask.get_size()
        superficie = pygame.Surface((w, h), pygame.SRCALPHA)

        # Nivel máximo según bebida
        if text in ("Opciones", "Salir"):
            nivel_max = h          # llenar hasta arriba
        else:
            nivel_max = int(h * 0.70)  # cerveza solo 70%
        velocidad = 0.35

        if hover:
            self.estado_llenado[text] = min(nivel_max, self.estado_llenado[text] + velocidad)
        else:
            self.estado_llenado[text] = 0
        nivel = int(self.estado_llenado[text])

        # Selección de bebida
        if text == "Salir":
            # Vino tinto 
            top = (180, 20, 40)
            bottom = (90, 0, 20)
            espuma_fija = False
            espuma_linea = False
            burbujas = False

        elif text == "Opciones":
            # Whisky 
            top = (210, 160, 70)
            bottom = (140, 90, 40)
            espuma_fija = False
            espuma_linea = False
            burbujas = False

        else:
            # Cerveza 
            top = (255, 210, 80)
            bottom = (215, 140, 30)
            espuma_fija = True
            espuma_linea = True
            burbujas = True

        # ===================
        # LÍQUIDO
        # ===================
        if nivel > 0:
            for y in range(h - nivel, h):
                t = (y - (h - nivel)) / max(nivel, 1)
                r = int(top[0] + (bottom[0] - top[0]) * t)
                g = int(top[1] + (bottom[1] - top[1]) * t)
                b = int(top[2] + (bottom[2] - top[2]) * t)
                pygame.draw.line(superficie, (r, g, b), (0, y), (w, y))

        # ===============================
        # ESPUMA EN LA CERVEZA 
        # ================================
        if espuma_linea and nivel > 0:
            espuma_y = h - nivel
            for x in range(0, w, 1):
                pygame.draw.circle(superficie, (255, 240, 150), (x, espuma_y), 4)

        # ===================================
        # ESPUMA FIJA ARRIBA (solo cerveza)
        # ===================================
        if espuma_fija and nivel > nivel_max * 0.40:
            espuma_altura = int(h * 0.35)
            progreso = (nivel - nivel_max * 0.40) / (nivel_max * 0.60)
            progreso = max(0, min(1, progreso))
            densidad = int(6 * progreso) + 1

            for capa in range(densidad):
                y = capa * 3
                if y < espuma_altura:
                    for x in range(0, w, 2):
                        pygame.draw.circle(superficie, (255, 255, 220, 240), (x, y), 3)

        # ==========================
        # BURBUJAS DE LA CERVEZA
        # =============================
        if burbujas and nivel > 0:
            for _ in range(12):
                bx = random.randint(0, w - 1)
                by = random.randint(0, nivel)
                pygame.draw.circle(superficie, (255, 255, 200, 180), (bx, h - by), 2)

        # Aplicar la máscara
        superficie.blit(mask, (0, 0), None, pygame.BLEND_RGBA_MULT)

        # ==================
        # CONTORNO NEGRO
        # ==================
        contorno = pygame.Surface((w + 4, h + 4), pygame.SRCALPHA)
        for dx in (-2, -1, 0, 1, 2):
            for dy in (-2, -1, 0, 1, 2):
                if dx != 0 or dy != 0:
                    sombra = self.font_button.render(text, True, (0, 0, 0))
                    contorno.blit(sombra, (2 + dx, 2 + dy))
        contorno.blit(superficie, (2, 2))
        return contorno

    # ==========================
    # DIBUJAR EL MENÚ
    # ==========================
    def draw(self):
        if self.fondo:
            self.window.blit(self.fondo, (0, 0))
        else:
            self.window.fill((20, 20, 20))
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        self.window.blit(overlay, (0, 0))

        # Título
        titulo = "Estoy perdido"
        sombra = self.font_title.render(titulo, True, (0, 0, 0))
        self.window.blit(sombra, (self.width//2 - sombra.get_width()//2 + 4, 120 + 4))
        title = self.font_title.render(titulo, True, (255, 255, 255))
        self.window.blit(title, (self.width//2 - title.get_width()//2, 120))
        mx, my = pygame.mouse.get_pos()

        for text, rect in self.buttons:
            hover = rect.collidepoint(mx, my)
            # Botellas
            botella = self.botellas.get(text)

            if botella:
                botella_h = rect.height
                botella_w = int(botella.get_width() * (botella_h / botella.get_height()))
                botella_scaled = pygame.transform.scale(botella, (botella_w, botella_h))
                bx = rect.x - botella_w - 20
                by = rect.y
                self.window.blit(botella_scaled, (bx, by))

                if hover:
                    brillo = pygame.Surface((botella_w, botella_h), pygame.SRCALPHA)
                    brillo.fill((255, 255, 255, 60))
                    self.window.blit(brillo, (bx, by))

            # Texto
            if hover:
                label = self.render_text_liquido(text, hover=True)
            else:
                label = self.font_button.render(text, True, (255, 255, 255))

            self.window.blit(label, (
                rect.x,
                rect.y + rect.height//2 - label.get_height()//2
            ))

        # Transición de fade-in
        if self.fade_alpha > 0:
            fade = pygame.Surface((self.width, self.height))
            fade.fill((0, 0, 0))
            fade.set_alpha(self.fade_alpha)
            self.window.blit(fade, (0, 0))
            self.fade_alpha = max(0, self.fade_alpha - 5)

    # ==============
    # CLICS
    # ==============
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            for text, rect in self.buttons:
                if rect.collidepoint(mx, my):
                    if self.sonido_burbujas:
                        self.sonido_burbujas.play()
                    return text
        return None
