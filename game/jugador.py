import random
from mazos import SET_LICORES

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        # Eventos del bar y los combos
        self.combo_preparado = None
        self.combo_activado = False
        self.fallo_forzado = 0.0

        # Estado general
        self.borracha = 0
        self.mano = []
        self.descartes = []
        self.efectos = []
        self.escudo = 0
        self.precision = 1.0
        self.evadir = False
        self.pasar_turno_flag = False
        self.ultimo_texto_combo = ""
        self.estado_actual = None
        self.saltar_proximo_robo = False

    # ============================================================
    # ESTADO DEL JUGADOR
    # ============================================================
    def estado(self):
        b = self.borracha
        if b < 40:
            return "sobrio"
        elif b < 70:
            return "contentillo"
        elif b < 90:
            return "tocado"
        else:
            return "ciego"

    def mensaje_estado(self, partida):
        estado = self.estado()
        if estado == self.estado_actual:
            return

        self.estado_actual = estado
        mensajes = {
            "sobrio": "Estás despejado como el agua. Todo bajo control.",
            "contentillo": "Una sonrisa tonta se te escapa… empiezas a sentirte valiente.",
            "tocado": "El mundo da un pequeño giro. Te cuesta enfocar, pero sigues en pie.",
            "ciego": "¡Uff! Te tambaleas. No sabes si estás jugando o bailando."
        }

        if partida and partida.escena:
            partida.escena.reproducir_sonido(f"estado_{estado}")

        if partida:
            partida.narrar(mensajes[estado])

    # ==============
    # EFECTOS
    # ==============
    def aplicar_efectos(self, partida):
        for efecto in self.efectos[:]:
            efecto.aplicar(self)
            if efecto.tick():
                if partida:
                    partida.narrar(f"{self.nombre} pierde el efecto: {efecto.nombre}")
                self.efectos.remove(efecto)

    # ===================
    # ROBO DE CARTAS
    # ===================
    def robar(self, mazo_central, cantidad=1, activar_eventos=True, partida=None):
        if self.saltar_proximo_robo:
            if partida:
                partida.narrar(f"{self.nombre} está demasiado desorientado y pierde su robo.")
            self.saltar_proximo_robo = False
            return
        
        for _ in range(cantidad):
            # Siempre usamos el mazo real de la partida
            mazo = partida.mazo_central

            # Si está vacío, intentamos reciclar
            if not mazo:
                if not partida.reciclar_mazo():
                    partida.narrar("No hay cartas para robar.")
                    return
                mazo = partida.mazo_central

            # Elegir carta con sesgo
            carta = self.robar_con_sesgo(mazo)
            mazo.remove(carta)

            # Eventos automáticos
            if activar_eventos and carta.tipo == "evento":
                carta.efecto(self, None, partida)
                self.descartes.append(carta)
                continue

            if not activar_eventos and carta.tipo == "evento":
                self.descartes.append(carta)
                continue
            self.mano.append(carta)
            
    def robar_con_sesgo(self, mazo):
        estado = self.estado()
        pool = mazo.copy()

        if estado == "sobrio":
            pool += [c for c in mazo if c.tipo in ["defensa", "accion"]]
        elif estado == "contentillo":
            pool += [c for c in mazo if c.tipo == "ataque"]
        elif estado == "tocado":
            pool += [c for c in mazo if c.tipo == "evento"]
        elif estado == "ciego":
            especiales = [c for c in mazo if c.nombre in ["Ataque Fuerte", "Chupito Infernal"]]
            if especiales:
                pool += especiales
            else:
                # Si no hay especiales, nunca dejamos el pool vacío
                pool = mazo.copy()

        # Si pool queda vacío por cualquier motivo
        if not pool:
            pool = mazo.copy()
        return random.choice(pool)

    # ====================
    # ESTADO FINAL
    # =====================
    def esta_borracho(self):
        return self.borracha >= 100

    # ======================
    # SISTEMA DE SETS
    # ======================
    def contar_sets(self):
        conteo = {licor: 0 for licor in SET_LICORES}
        for c in self.mano:
            if c.nombre in conteo:
                conteo[c.nombre] += 1
        return conteo

    def tiene_pareja(self):
        for licor, n in self.contar_sets().items():
            if n >= 2:
                return licor
        return None

    def tiene_trio(self):
        for licor, n in self.contar_sets().items():
            if n >= 3:
                return licor
        return None

    def tiene_set_completo(self):
        conteo = self.contar_sets()
        return all(conteo[licor] >= 1 for licor in SET_LICORES)

    # ============================================================
    # SINERGIAS ENTRE CARTAS SET Y CARTAS EXISTENTES Y COMBOS
    # ============================================================
    def aplicar_sinergias(self, carta, rival, partida):

        # ================
        # SINERGIAS
        # ================
        # Vermut + Ataques = +10 borrachera
        if carta.tipo == "ataque":
            if any(c.nombre == "Vermut" for c in self.mano):
                rival.borracha += 10
                texto = "SINERGIA: Vermut potencia tu ataque → +10 borrachera."
                partida.narrar(texto)

        # Orujo + Ataque Fuerte = +15 borrachera
        if carta.nombre == "Ataque Fuerte":
            if any(c.nombre == "Orujo" for c in self.mano):
                rival.borracha += 15
                texto = "SINERGIA: ¡Orujo ardiente! Ataque Fuerte gana +15 borrachera."
                partida.narrar(texto)

        # Pacharán + Defensa = escudo +10
        if carta.tipo == "defensa":
            if any(c.nombre == "Pacharán" for c in self.mano):
                self.escudo += 10
                texto = "SINERGIA: Pacharán te da valor → escudo +10."
                partida.narrar(texto)

        # Anís + Evento = +5 borrachera
        if carta.tipo == "evento":
            if any(c.nombre == "Anís" for c in self.mano):
                rival.borracha += 5
                texto = "SINERGIA: El Anís potencia el evento → +5 borrachera."
                partida.narrar(texto)

        # Set incompleto (3 licores distintos) = +30 borrachera
        tipos = {c.nombre for c in self.mano if c.nombre in SET_LICORES}
        if len(tipos) == 3:
            rival.borracha += 30
            texto = "SINERGIA: Casi un set completo → +30 borrachera extra."
            partida.narrar(texto)

    def activar_combo_auto(self, rival, partida):
        self.combo_activado = False
        self.ultimo_texto_combo = ""

        # ===================
        # SET COMPLETO
        # ===================
        if self.tiene_set_completo():
            usados = {licor: 0 for licor in SET_LICORES}
            nuevas = []

            for c in self.mano:
                if c.nombre in usados and usados[c.nombre] == 0:
                    self.descartes.append(c)
                    usados[c.nombre] = 1
                else:
                    nuevas.append(c)
            self.mano = nuevas

            daño = random.randint(40, 60)
            rival.borracha += daño

            texto = (
                f"{self.nombre} activa SET COMPLETO → ¡CUBATA LEGENDARIO!\n"
                f"{rival.nombre} recibe +{daño} borrachera."
            )
            partida.narrar(texto)
            self.combo_activado = True
            self.ultimo_texto_combo = texto
            return True

        # ====================
        # TRÍO
        # ====================
        licor_trio = self.tiene_trio()
        if licor_trio:
            usadas = 0
            nuevas = []

            for c in self.mano:
                if c.nombre == licor_trio and usadas < 3:
                    self.descartes.append(c)
                    usadas += 1
                else:
                    nuevas.append(c)

            self.mano = nuevas

            texto = (
                f"{self.nombre} activa TRÍO → BORRACHERA TÁCTICA\n"
                f"Robas una carta y el rival pierde una."
            )
            partida.narrar(texto)

            if rival.mano:
                elegida = random.choice(rival.mano)
                rival.mano.remove(elegida)
                self.mano.append(elegida)

            if rival.mano:
                perdida = random.choice(rival.mano)
                rival.mano.remove(perdida)
                rival.descartes.append(perdida)

            daño = random.randint(25, 30)
            rival.borracha += daño
            rival.saltar_proximo_robo = True

            self.combo_activado = True
            self.ultimo_texto_combo = texto
            return True

        # ====================
        # PAREJA
        # ====================
        licor_pareja = self.tiene_pareja()
        if licor_pareja:
            usadas = 0
            nuevas = []

            for c in self.mano:
                if c.nombre == licor_pareja and usadas < 2:
                    self.descartes.append(c)
                    usadas += 1
                else:
                    nuevas.append(c)
            self.mano = nuevas

            texto = (
                f"{self.nombre} activa PAREJA → DOBLE CHUPITO\n"
                f"Robas una carta y el rival pierde una."
            )
            partida.narrar(texto)

            if rival.mano:
                carta_robada = random.choice(rival.mano)
                rival.mano.remove(carta_robada)
                self.mano.append(carta_robada)

            if rival.mano:
                perdida = random.choice(rival.mano)
                rival.mano.remove(perdida)
                rival.descartes.append(perdida)

            rival.borracha += 18
            self.combo_activado = True
            self.ultimo_texto_combo = texto
            return True
        return False
