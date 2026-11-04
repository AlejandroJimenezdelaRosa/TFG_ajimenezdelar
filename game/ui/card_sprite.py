import pygame

class CardSprite:
    def __init__(self, carta, x, y):
        self.carta = carta
        self.image = pygame.image.load(f"assets/cards/{carta.nombre}.png")
        self.rect = self.image.get_rect(topleft=(x, y))

    def handle_event(self, event, partida, ui):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Jugar la carta
                idx = partida.jugador.mano.index(self.carta)
                partida.jugador.jugar_carta(idx, partida.rival, partida)
                ui.refresh_cards()

    def draw(self, window):
        window.blit(self.image, self.rect)
