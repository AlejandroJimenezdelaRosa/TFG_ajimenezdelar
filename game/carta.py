import pygame
import os

class Carta:
    def __init__(self, nombre, tipo, descripcion, efecto):
        self.nombre = nombre
        self.tipo = tipo
        self.descripcion = descripcion
        self.efecto = efecto
        self.img = None
        self.img_small = None
        self.img_big = None
        self.cargar_imagen(nombre)

    def cargar_imagen(self, nombre):
        archivo = (
            nombre.lower()
            .replace(" ", "_")
            .replace("í", "i")
            .replace("á", "a")
            .replace("é", "e")
            .replace("ó", "o")
            .replace("ú", "u")
        ) + ".png"

        ruta = os.path.join("game", "ui", "assets", "objetos", archivo)
        if os.path.exists(ruta):
            img_original = pygame.image.load(ruta).convert_alpha()
            self.img = pygame.transform.smoothscale(img_original, (128, 180))
            self.img_small = pygame.transform.smoothscale(img_original, (96, 135))
            self.img_big = pygame.transform.smoothscale(img_original, (300, 420))
        else:
            base = pygame.Surface((128, 180), pygame.SRCALPHA)
            base.fill((80, 80, 80))
            pygame.draw.rect(base, (200, 200, 200), base.get_rect(), 3)
            self.img = base
            self.img_small = pygame.transform.smoothscale(base, (96, 135))
            self.img_big = pygame.transform.smoothscale(base, (300, 420))

    def usar(self, usuario, rival, partida):
        self.efecto(usuario, rival, partida)
