import pygame
from ui.dialogue_box import DialogueBox

class UIManager:
    def __init__(self, window, partida):
        self.window = window
        self.partida = partida
        self.dialogue = DialogueBox(window.get_width(), window.get_height())

    def handle_event(self, event):
        self.dialogue.handle_event(event)

    def update(self):
        pass

    def draw(self):
        # NO borrar la pantalla
        self.dialogue.draw(self.window)
