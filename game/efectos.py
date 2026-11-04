class EfectoPersistente:
    def __init__(self, nombre, modificador, duracion):
        self.nombre = nombre
        self.modificador = modificador  
        self.duracion = duracion

    def aplicar(self, jugador):
        for stat, valor in self.modificador.items():
            setattr(jugador, stat, getattr(jugador, stat) + valor)

    def tick(self):
        self.duracion -= 1
        return self.duracion <= 0
