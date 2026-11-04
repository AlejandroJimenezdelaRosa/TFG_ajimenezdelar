from mazos import crear_mazo_unico
from jugador import Jugador
import random

# ============================================================
# CLASE PARTIDA CON LA LÓGICA DE JUEGO Y NARRACIÓN PARA UI
# ============================================================
class Partida:
    def __init__(self, capitulo=1):
        self.capitulo = capitulo
        self.turno = "jugador"
        self.turno_num = 1
        self.resultado = None
        self.decision_cap1 = None
        
        # Referencia a la escena de combate
        self.escena = None

        # Rival según el capítulo
        self.rival = self.seleccionar_rival(capitulo)

        if not hasattr(self, "ui"):
            self.ui = None

        # Jugador principal
        self.jugador = Jugador("Protagonista")

        # Crear el mazo central
        self.mazo_central = crear_mazo_unico()

        # Robar las cartas iniciales
        for _ in range(5):
            self.jugador.robar(self.mazo_central, partida=self)
            self.rival.robar(self.mazo_central, partida=self)

    # =====================================================
    # SISTEMA DE NARRACIÓN (UI + EL RECUADRO DE ACCIÓN)
    # =====================================================
    def narrar(self, texto):
        """
        Envía texto a la UI si existe.
        Si hay escena de combate activa, también actualiza el recuadro de acción.
        Si no hay UI, imprime en consola.
        """
        # 1) Si hay UI narrativa
        if self.ui is not None and hasattr(self.ui, "dialogue"):
            self.ui.dialogue.add_message(texto)

        # 2) Si hay escena de combate, se envia al recuadro de acción
        if self.escena is not None:
            self.escena.iniciar_texto_accion(texto)

        # 3) Consola 
        if self.ui is None:
            print(texto)

    # ===================================
    # SELECCIÓN DE RIVAL POR CAPÍTULO
    # ===================================
    def seleccionar_rival(self, capitulo):
        if capitulo == 1:
            return Jugador("Desconocido")
        if capitulo == 2:
            return Jugador("Francisco")
        if capitulo == 3:
            return Jugador("Británico")
        if capitulo == 4:
            return Jugador("Alemán")
        if capitulo == 5:
            return Jugador("Italiano")
        return Jugador("Rival Misterioso")

    # ============================
    # RECICLAR MAZO
    # ============================
    def reciclar_mazo(self):
        if not self.jugador.descartes and not self.rival.descartes:
            return False

        self.narrar("El mazo se ha agotado. El camarero recoge las cartas del suelo…")

        nuevo_mazo = self.jugador.descartes + self.rival.descartes
        self.jugador.descartes = []
        self.rival.descartes = []

        random.shuffle(nuevo_mazo)
        self.mazo_central = nuevo_mazo
        return True

    # =====================
    # FIN DE PARTIDA
    # ====================
    def comprobar_fin(self):

    # Derrota del jugador
        if self.jugador.esta_borracho():
            self.resultado = "derrota"
            self.narrar("Te desplomas sobre la mesa. ¡Has perdido!")
            return True

        # Victoria del jugador
        if self.rival.esta_borracho():
            self.resultado = "victoria"
            self.narrar(f"{self.rival.nombre} cae redondo. ¡Has ganado!")
            return True

        return False
