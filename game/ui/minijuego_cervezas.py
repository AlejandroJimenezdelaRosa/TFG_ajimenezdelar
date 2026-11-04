import pygame

#INCORPORAR SI HAY TIEMPO SINO NADA
class MinijuegoCervezas:
    def __init__(self, partida):
        self.partida = partida

        self.rondas_totales = 5
        self.ronda_actual = 0  # empezamos en 0, iremos sumando

        self.barra_altura = 0
        self.barra_max = 300
        self.barra_limite = 240  # límite rojo

        self.velocidad_subida = 4
        self.velocidad_bajada = 2

        self.resultado = None

        self.font = pygame.font.SysFont("Arial", 32)

        self.pulsando_antes = False  # para detectar soltado

    def update(self, window, keys):

        window.fill((20, 20, 20))

        texto_ronda = self.font.render(
            f"Ronda {self.ronda_actual + 1} / {self.rondas_totales}",
            True, (255, 255, 255)
        )
        window.blit(texto_ronda, (20, 20))

        pulsando = keys[pygame.K_SPACE]

        # Subir / bajar barra
        if pulsando:
            self.barra_altura += self.velocidad_subida
        else:
            self.barra_altura -= self.velocidad_bajada

        if self.barra_altura < 0:
            self.barra_altura = 0
        if self.barra_altura > self.barra_max:
            self.barra_altura = self.barra_max

        # FALLO: te pasas del límite mientras pulsas
        if pulsando and self.barra_altura >= self.barra_limite:
            self.resultado = "fallo"
            return "fin_minijuego"

        # ÉXITO DE UNA JARRA: sueltas después de haber pulsado, sin pasarte
        if not pulsando and self.pulsando_antes:
            # Solo cuenta si has llenado algo 
            if 40 < self.barra_altura < self.barra_limite:
                self.ronda_actual += 1
                self.barra_altura = 0

                if self.ronda_actual >= self.rondas_totales:
                    self.resultado = "exito"
                    return "fin_minijuego"

        self.pulsando_antes = pulsando

        # Dibujo barra
        pygame.draw.rect(
            window,
            (150, 75, 0),
            (600, 500 - self.barra_altura, 80, self.barra_altura)
        )

        pygame.draw.line(
            window,
            (255, 0, 0),
            (580, 500 - self.barra_limite),
            (700, 500 - self.barra_limite),
            4
        )

        texto = self.font.render("Mantén ESPACIO para llenar la jarra", True, (255, 255, 255))
        window.blit(texto, (350, 600))

        texto2 = self.font.render("Suelta antes del límite rojo", True, (255, 255, 255))
        window.blit(texto2, (380, 640))

        return None
