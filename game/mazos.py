import random
from carta import Carta

# ==========================
# CONSTANTES
# ==========================

SET_LICORES = ["Anís", "Pacharán", "Orujo", "Vermut"]

# ===================================================
# SISTEMA DE PRECISIÓN Y MODIFICADORES POR ESTADO
# ==================================================
def modificador_estado(usuario):
    estado = usuario.estado()

    if estado == "sobrio":
        return 0.10
    if estado == "contentillo":
        return 0.05
    if estado == "tocado":
        return -0.10
    if estado == "ciego":
        return -0.20
    return 0

def calcular_precision(usuario):
    base = 1 - (usuario.borracha / 200)
    mod = modificador_estado(usuario)
    return max(0.40, min(1.0, base + mod))

# ===================================
# DAÑO VARIABLE POR CAUSAS Y ESTADO
# ===================================
def daño_variable(base, usuario):
    variacion = int(usuario.borracha * 0.15)

    estado = usuario.estado()
    if estado == "tocado":
        variacion = int(variacion * 1.3)
    elif estado == "ciego":
        variacion = int(variacion * 1.6)

    return base + random.randint(-variacion, variacion)

# ============================================================
# ATAQUE COMPLETO CON SISTEMA DE MENSAJES, ROLES Y SINERGIAS
# ============================================================
def ataque_con_precision(usuario, rival, partida, base, tipo="normal", ignora_escudo=False):
    if hasattr(usuario, "fallo_forzado") and usuario.fallo_forzado > 0:
        if random.random() < usuario.fallo_forzado:
            partida.narrar(f"{usuario.nombre} falla por la oscuridad del bar.")
            usuario.fallo_forzado = 0
            return
        usuario.fallo_forzado = 0

    # ==========================
    # 0. SINERGIAS MANUALES
    # =========================
    sinergia_bonus = 0
    combo = getattr(usuario, "combo_preparado", None)

    if combo == "chiste":
        sinergia_bonus += 5
    if combo == "agua":
        ignora_escudo = True
    if combo == "fumar":
        usuario.precision = min(1.0, usuario.precision + 0.10)

    if hasattr(usuario, "combo_preparado"):
        usuario.combo_preparado = None

    # ===========================
    # 1. Fallo por precisión
    # ============================
    if random.random() > calcular_precision(usuario):
        partida.narrar(f"{usuario.nombre} intenta atacar… pero falla estrepitosamente.")
        if partida and partida.escena:
            partida.escena.reproducir_sonido("fallo")
        return

    # ===========================
    # 2. Sonido del ataque
    # ===========================
    if partida and partida.escena:
        if tipo == "suave":
            partida.escena.reproducir_sonido("ataque_suave")
        elif tipo == "medio":
            partida.escena.reproducir_sonido("ataque_medio")
        elif tipo == "fuerte":
            partida.escena.reproducir_sonido("ataque_fuerte")

    # ================================
    # 3. Construcción del mensaje
    # ===============================
    resumen = []
    resumen.append(f"{usuario.nombre} usó {tipo.upper()}.")
    resumen.append(f"Daño base: {base}.")
    estado = usuario.estado()
    resumen.append(f"Estado actual: {estado}.")

    # ==================
    # 4. Evadir
    # ==================
    if rival.evadir:
        if random.random() < 0.40:
            resumen.append(f"{rival.nombre} esquiva el ataque por los pelos.")
            rival.evadir = False
            partida.narrar("\n".join(resumen))
            return
        else:
            resumen.append(f"{rival.nombre} intenta esquivar, pero falla.")
            rival.evadir = False

    # =================
    # 5. Escudo
    # =================
    if rival.escudo > 0 and not ignora_escudo:
        rival.escudo -= 1
        resumen.append(f"{rival.nombre} bloquea el ataque con un escudo improvisado.")
        partida.narrar("\n".join(resumen))
        return

    # ====================
    # 6. Daño variable
    # ====================
    daño = daño_variable(base, usuario)

    # ===========================
    # 7. Efectos por estado
    # ===========================
    if estado == "sobrio" and random.random() < 0.05:
        daño += 10
        resumen.append("Golpe limpio (+10).")
    elif estado == "contentillo" and random.random() < 0.08:
        daño += 5
        resumen.append("Te vienes arriba (+5).")
    elif estado == "tocado" and random.random() < 0.12:
        daño //= 2
        resumen.append("Ataque torpe (daño reducido a la mitad).")
    elif estado == "ciego" and random.random() < 0.18:
        daño = int(daño * 1.5)
        usuario.borracha += 5
        resumen.append("Golpe descontrolado (+50% daño, +5 borrachera).")

    # ===========================
    # 8. Efectos por tipo
    # ===========================
    if tipo == "chiste":
        rival.precision = max(0.40, rival.precision - 0.10)
        resumen.append("El rival pierde precisión (-10%).")
        usuario.combo_preparado = "chiste"

    if tipo == "fuerte":
        if random.random() < 0.10:
            usuario.borracha += 5
            resumen.append("Tropiezas (+5 borrachera).")
        if random.random() < 0.10:
            daño += 20
            resumen.append("¡GOLPE CRÍTICO! (+20).")
            if partida and partida.escena:
                partida.escena.reproducir_sonido("critico")

    # ===========================
    # 9. SINERGIAS MANUALES
    # ===========================
    if sinergia_bonus > 0:
        daño += sinergia_bonus
        resumen.append(f"Sinergia aplicada (+{sinergia_bonus}).")

    # ===========================
    # 10. Aplicar daño final
    # ==========================
    rival.borracha += daño
    resumen.append(f"Daño final aplicado: +{daño} borrachera.")

    # ==============================
    # 11. Crítico por borrachera
    # ===============================
    crit_chance = 0.10 + getattr(usuario, "critico_bonus", 0)

    if random.random() < crit_chance:
        rival.borracha += 15
        resumen.append("¡CRÍTICO POR BORRACHERA! (+15).")
        if partida and partida.escena:
            partida.escena.reproducir_sonido("critico")

    # ====================
    # 12. Doble golpe
    # ======================
    if usuario.borracha >= 90 and random.random() < 0.20:
        rival.borracha += base
        resumen.append(f"¡DOBLE GOLPE! (+{base}).")

    # ============================
    # 13. Enviar mensaje final
    # ============================
    partida.narrar("\n".join(resumen))

def efecto_ataque(base, tipo="normal", ignora_escudo=False):
    def _efecto(usuario, rival, partida):
        ataque_con_precision(usuario, rival, partida, base, tipo, ignora_escudo)
    return _efecto

# ===================================
# EVENTOS DEL BAR (cada X turnos)
# ==================================
def evento_del_bar(partida, jugador, rival):
    eventos = [
        ("La música sube", "musica", "Tu borrachera baja 5 puntos y recuperas precisión"),
        ("El camarero te anima", "camarero", "Ganas +5 borrachera"),
        ("Se apagan las luces", "luces", "Tu precisión baja (fallo forzado 35%)"),
        ("Un borracho te empuja", "empujon", "Ganas +10 borrachera"),
        ("Llega la policía", "policia", "Pierdes el turno"),
    ]

    # Elegir el evento aleatorio
    nombre, tipo, descripcion = random.choice(eventos)

    # Mensaje completo para el recuadro de texto
    mensaje = (
        f"EVENTO DEL BAR: {nombre}\n"
        f"Efecto: {descripcion}"
    )

    # Aplicar los efectos reales del evento
    if tipo == "musica":
        jugador.borracha = max(0, jugador.borracha - 5)
        jugador.precision = 1.0
        jugador.combo_preparado = "musica"
    elif tipo == "camarero":
        jugador.borracha += 5
    elif tipo == "luces":
        jugador.fallo_forzado = 0.35
    elif tipo == "empujon":
        jugador.borracha += 10
    elif tipo == "policia":
        jugador.pasar_turno_flag = True

    # Mostrar mensaje en el log y en el recuadro de acción
    partida.narrar(mensaje)
    if partida and partida.escena:
        partida.escena.iniciar_texto_accion(mensaje)

# ==========================
# ATAQUES ESPECIALES
# ==========================
def brindis_mortal(usuario, rival, partida):
    daño = 12
    if rival.borracha >= 70:
        daño += 20

    rival.borracha += daño

    partida.narrar(
        f"{usuario.nombre} propone un BRINDIS MORTAL.\n"
        f"{rival.nombre} recibe +{daño} borrachera."
    )

def chupito_infernal(usuario, rival, partida):
    rival.borracha += 30
    usuario.borracha += 10

    partida.narrar(
        f"{usuario.nombre} bebe un CHUPITO INFERNAL.\n"
        f"{rival.nombre} recibe +30 borrachera.\n"
        f"{usuario.nombre} recibe +10 borrachera."
    )

# ==============================
# CURACIONES Y DEFENSAS
# =============================
def curacion(usuario, rival, partida):
    antes = usuario.borracha
    usuario.borracha = max(0, usuario.borracha - 25)
    recuperado = antes - usuario.borracha

    partida.narrar(
        f"{usuario.nombre} se refresca la cara.\n"
        f"Recupera {recuperado} borrachera."
    )

def agua_del_tiempo(usuario, rival, partida):
    usuario.borracha = max(0, usuario.borracha - 20)
    usuario.precision = min(1.0, usuario.precision + 0.10)
    usuario.combo_preparado = "agua"

    partida.narrar(
        f"{usuario.nombre} bebe Agua del Tiempo.\n"
        f"Recupera 20 borrachera y gana precisión temporal."
    )

def salir_a_fumar(usuario, rival, partida):
    usuario.evadir = True
    usuario.borracha = max(0, usuario.borracha - 10)
    usuario.combo_preparado = "fumar"

    partida.narrar(
        f"{usuario.nombre} sale a despejarse.\n"
        f"Evita daño este turno, roba 1 carta y recupera 10 borrachera."
    )

    usuario.robar(partida.mazo_central, 1, activar_eventos=False, partida=partida)

def favor(usuario, rival, partida):
    if not rival.mano:
        partida.narrar("El rival no tiene cartas.")
        return

    carta = random.choice(rival.mano)
    rival.mano.remove(carta)
    usuario.mano.append(carta)

    partida.narrar(f"{usuario.nombre} roba {carta.nombre} del rival.")

def defensa_reducir(usuario, rival, partida):
    antes = usuario.borracha
    usuario.borracha = max(0, usuario.borracha - 15)
    recuperado = antes - usuario.borracha

    partida.narrar(
        f"{usuario.nombre} se estabiliza.\n"
        f"Pierde {recuperado} borrachera."
    )

# ==============
# EVENTOS
# ===============

def chupito_fuego(usuario, rival, partida):
    estado = usuario.estado()
    valores = {"sobrio": 10, "contentillo": 15, "tocado": 20, "ciego": 25}
    daño = valores[estado]

    usuario.borracha += daño
    partida.narrar(
        f"Chupito de Fuego para {usuario.nombre}.\n"
        f"Estado: {estado}.\n"
        f"Recibe +{daño} borrachera."
    )

def ruleta_del_bar(usuario, rival, partida):
    estado = usuario.estado()

    opciones = {
        "sobrio": ["+10", "-10", "robar1"],
        "contentillo": ["+15", "-15", "robar1", "perder1"],
        "tocado": ["+20", "-10", "robar2", "perder2"],
        "ciego": ["+25", "-5", "perder3", "explosion"]
    }

    efecto = random.choice(opciones[estado])
    mensaje = [f"Ruleta del Bar ({estado}). Resultado: {efecto}"]
    if efecto.startswith("+"):
        valor = int(efecto[1:])
        objetivo = rival if rival else usuario
        objetivo.borracha += valor
        mensaje.append(f"{objetivo.nombre} recibe +{valor} borrachera.")
    elif efecto.startswith("-"):
        valor = int(efecto[1:])
        usuario.borracha = max(0, usuario.borracha - valor)
        mensaje.append(f"{usuario.nombre} pierde {valor} borrachera.")
    elif efecto == "robar1":
        usuario.robar(partida.mazo_central, 1, activar_eventos=False, partida=partida)
        mensaje.append("Robas 1 carta.")
    elif efecto == "robar2":
        usuario.robar(partida.mazo_central, 2, activar_eventos=False, partida=partida)
        mensaje.append("Robas 2 cartas.")
    elif efecto == "perder1":
        if usuario.mano:
            perdida = usuario.mano.pop(0)
            usuario.descartes.append(perdida)
            mensaje.append(f"Pierdes {perdida.nombre}.")
    elif efecto == "perder2":
        for _ in range(2):
            if usuario.mano:
                perdida = usuario.mano.pop(0)
                usuario.descartes.append(perdida)
        mensaje.append("Pierdes 2 cartas.")
    elif efecto == "perder3":
        for _ in range(3):
            if usuario.mano:
                perdida = usuario.mano.pop(0)
                usuario.descartes.append(perdida)
        mensaje.append("Pierdes 3 cartas.")
    elif efecto == "explosion":
        usuario.borracha += 15
        if rival:
            rival.borracha += 15
        mensaje.append("¡Explosión! Ambos reciben +15 borrachera.")
    partida.narrar("\n".join(mensaje))

def explosion_botellines(usuario, rival, partida):
    daño = 10 if usuario.borracha < 90 else 15
    usuario.borracha += daño
    if rival:
        rival.borracha += daño

    partida.narrar(
        f"¡Explosión de botellines!\n"
        f"Ambos reciben +{daño} borrachera."
    )

# =======================================
# MAZO COMPLETO CON LAS CARTAS DEL JUEGO
# =========================================
def crear_mazo_unico():
    mazo = []

    # Evwentos del bar
    mazo.append(Carta("Chupito de Fuego", "evento", "Evento automático", chupito_fuego))
    mazo.append(Carta("Ruleta del Bar", "evento", "Evento aleatorio", ruleta_del_bar))
    mazo.append(Carta("Explosión de Botellines", "evento", "Evento aleatorio", explosion_botellines))
    mazo.append(Carta("Noche Loca", "evento", "Evento inesperado", explosion_botellines))

    # Acciones de curación y defensa
    for _ in range(4):
        mazo.append(Carta("Curación", "accion", "Recuperas 25 borrachera", curacion))

    for _ in range(3):
        mazo.append(Carta("Agua del Tiempo", "accion", "Cura 20 y da precisión", agua_del_tiempo))

    for _ in range(3):
        mazo.append(Carta("Salir a Fumar", "accion", "Evitas daño, robas 1 y curas 10", salir_a_fumar))

    for _ in range(2):
        mazo.append(Carta("Favor", "accion", "Robas una carta al rival", favor))

    # Ataques 
    for _ in range(5):
        mazo.append(Carta("Ataque Suave", "ataque", "+10 borrachera", efecto_ataque(10, "suave")))

    for _ in range(5):
        mazo.append(Carta("Ataque Medio", "ataque", "+15 borrachera", efecto_ataque(15, "medio")))

    for _ in range(4):
        mazo.append(Carta("Ataque Fuerte", "ataque", "+20 borrachera + efectos", efecto_ataque(20, "fuerte")))

    for _ in range(4):
        mazo.append(Carta("Chiste Malo", "ataque", "Reduce precisión del rival", efecto_ataque(5, "chiste")))

    # Especiales únicos
    mazo.append(Carta("Brindis Mortal", "ataque", "Ataque especial", brindis_mortal))
    mazo.append(Carta("Chupito Infernal", "ataque", "Daño alto pero te afecta también", chupito_infernal))

    # Defensas
    for _ in range(8):
        mazo.append(Carta("Resistir", "defensa", "Reduce 15 borrachera", defensa_reducir))

    # Sets de licores 
    for nombre in SET_LICORES:
        for _ in range(5):
            mazo.append(Carta(nombre, "set", "Carta de set", lambda u, r, p: None))
            
    random.shuffle(mazo)
    return mazo
