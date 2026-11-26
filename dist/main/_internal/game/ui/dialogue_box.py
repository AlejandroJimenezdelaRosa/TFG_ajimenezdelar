import pygame

class DialogueBox:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.box_rect = pygame.Rect(50, height - 280, width - 100, 230)
        self.font = pygame.font.SysFont("arial", 28)
        self.text = ""
        self.visible = False
        self.queue = []
        self.options = []
        self.selected_option = 0
        self.showing_options = False
        self.option_chosen = None

    def set_options(self, options):
        self.options = options
        self.selected_option = 0
        self.showing_options = True

    def confirm_option(self):
        if not self.showing_options:
            return None
        self.option_chosen = self.selected_option
        self.clear_options()
        self.next_message()
        return self.option_chosen

    def clear_options(self):
        self.options = []
        self.selected_option = 0
        self.showing_options = False
        
    def add_message(self, msg):
        self.queue.append(msg)
        if not self.visible:
            self.next_message()

    def next_message(self):
        if self.queue:
            self.text = self.queue.pop(0)
            self.visible = True
        else:
            self.visible = False

    def handle_event(self, event):

        if not self.visible:
            return

        # Si hay opciones abiertas, no permite avanzar diálogo
        if self.showing_options:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = max(
                        0,
                        self.selected_option - 1
                    )

                elif event.key == pygame.K_DOWN:
                    self.selected_option = min(
                        len(self.options) - 1,
                        self.selected_option + 1
                    )
            return

        # Avance de los diálogos
        if event.type == pygame.MOUSEBUTTONDOWN or \
        (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            self.next_message()

    def draw(self, window):
        if not self.visible:
            return

        pygame.draw.rect(window, (0, 0, 0), self.box_rect)
        pygame.draw.rect(window, (255, 255, 255), self.box_rect, 3)

        words = self.text.split(" ")
        line = ""
        y = self.box_rect.y + 20
        lineas = []

        for word in words:
            test_line = line + word + " "
            if self.font.size(test_line)[0] < self.box_rect.width - 40:
                line = test_line
            else:
                lineas.append(line)
                line = word + " "
        lineas.append(line)

        # Si hay opciones mostramos menos líneas de texto
        max_lineas = 2 if self.showing_options else len(lineas)

        for linea in lineas[:max_lineas]:
            rendered = self.font.render(
                linea,
                True,
                (255, 255, 255)
            )

            window.blit(
                rendered,
                (self.box_rect.x + 20, y)
            )
            y += 35

        if self.showing_options:
            # Posición fija para las opciones
            opciones_y = self.box_rect.y + 90

            for i, option in enumerate(self.options):
                color = (
                    (255, 255, 0)
                    if i == self.selected_option
                    else (255, 255, 255)
                )

                prefix = "> " if i == self.selected_option else "   "
                render = self.font.render(
                    prefix + option,
                    True,
                    color
                )

                window.blit(
                    render,
                    (
                        self.box_rect.x + 40,
                        opciones_y + i * 30
                    )
                )
