import pygame

class HealthBar: #Ahora se llama PuntosAlcohol por el mensaje de que es un medidor de borrachera, no de vida
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = 0

    def set_value(self, value):
        self.value = max(0, min(100, value))

    def draw(self, window):
        pygame.draw.rect(window, (50, 50, 50), self.rect)
        fill = pygame.Rect(self.rect.x, self.rect.y, self.rect.width * (self.value / 100), self.rect.height)
        pygame.draw.rect(window, (200, 50, 50), fill)
